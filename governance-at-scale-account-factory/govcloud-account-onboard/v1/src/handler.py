# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, logging
from betterboto import client as betterboto_client
import os
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format="%(levelname)s %(threadName)s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)

# get the org access role from the environment variables
organization_account_access_role = os.environ.get("ORGANIZATION_ACCOUNT_ACCESS_ROLE")


def handler(event, context):
    logger.info("API Called from Commercial SNS")
    logger.info(f"Incomming Event: {event}")

    try:
        # parse the incoming payload
        payload = json.loads(json.loads(event["body"]))
        logger.info(f"Payload: {payload}")

        # only work with GovCloud accounts
        if payload.get("AccountPartition") == "GovCloud":
            # get the necessary values from the payload
            account_id = payload.get("AccountId")
            puppet_account_id = payload.get("PuppetAccountId")
            target_ou = payload.get("ManagedOrganizationalUnit")

            # use the Organizations client
            with betterboto_client.ClientContextManager(
                "organizations"
            ) as organizations:
                account_exists = False
                try:
                    # check if the account is already in an organization
                    result = organizations.list_parents_single_page(ChildId=account_id)
                    if len(result.get("Parents", [])) > 0:
                        logger.info(
                            "The account is already in an organization. No need to send an invite."
                        )
                        account_exists = True
                except Exception as ex:
                    # an error is thrown when an account does not have parents and
                    # is therefore not part of an organization
                    logger.info(
                        "The account is not in an organization. Proceeding to invite the account to the organization"
                    )
                    account_exists = False

                # only add the account to the organization if it isn't already a
                # part of the organization
                if not account_exists:
                    # invite the new account to the organization
                    response = organizations.invite_account_to_organization(
                        Target={"Id": account_id, "Type": "ACCOUNT"},
                        Notes="You have been invited to our GovCloud Organization",
                    )
                    logger.info(f"Invitation Sent: {response}")
                    # record the Handshake ID from the reponse
                    handshake_id = response["Handshake"]["Id"]
                    # accept the handshake as the member account
                    accept_handshake(account_id, handshake_id)

            # move the account to the correct organizational unit
            move_to_ou(account_id, target_ou)
            # bootstrap the account from the puppet account
            bootstrap_account(account_id, puppet_account_id)

            # inform the caller that the account was successful onboarded
            return {
                "statusCode": 200,
                "body": json.dumps("The account has been onboard successfully"),
            }

        # return a 404 status informing the caller that the account is of the wrong type
        return {
            "statusCode": 404,
            "body": json.dumps(
                "The account is not a GovCloud account. No invitation was sent"
            ),
        }
    except Exception as ex:
        # log the error and the stack trace
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        # return a 500 error to the caller
        return {
            "statusCode": 500,
            "body": json.dumps(
                "Oops, something went wrong. The attempt to invite the account to the organization failed."
            ),
        }


def accept_handshake(account_id, handshake_id):
    # build the ARN for the assumable role in the member account
    organization_account_access_role_arn = "arn:aws-us-gov:iam::{}:role/{}".format(
        account_id, organization_account_access_role
    )

    # use the cross-account Organizations client with the assumable role
    with betterboto_client.CrossAccountClientContextManager(
        "organizations",
        organization_account_access_role_arn,
        "accept_handshake",
    ) as member_organization:
        logger.info("Accepting the invitation")

        # accept the invitation to join the organization
        response = member_organization.accept_handshake(HandshakeId=handshake_id)
        logger.info(f"Handshake Response: {response}")


def move_to_ou(account_id, target_ou):
    logger.info(f"Moving account {account_id} to OU {target_ou}")

    # use the Organizations client in the current account
    with betterboto_client.ClientContextManager("organizations") as root_org:
        # list the parents for the account and ensure there is only one parent
        result = root_org.list_parents_single_page(ChildId=account_id)
        if len(result.get("Parents", [])) != 1:
            raise Exception(
                f"There were unexpected parents for the account_id {account_id}: {json.dumps(result)}"
            )

        current_ou = result.get("Parents")[0].get("Id")
        # if the account is already in the correct OU, just log and continue gracefully
        if current_ou == target_ou:
            logger.info("The account is already in the correct OU")
        elif str(target_ou) != "None" and current_ou != target_ou:
            logger.info("Moving account to new OU")

            # make sure there is only one root account
            response = root_org.list_roots()
            if len(response.get("Roots")) != 1:
                raise Exception("nRoots: {}".format(len(response.get("Roots"))))

            if str(target_ou).startswith("/"):
                # if the OU is using the path format, convert it to an OU ID
                target = root_org.convert_path_to_ou(target_ou)
            else:
                target = target_ou

            # move the account to the target OU
            root_org.move_account(
                AccountId=account_id,
                SourceParentId=current_ou,
                DestinationParentId=target,
            )

        logger.info(f"Account {account_id} was moved to OU {target}")


def bootstrap_account(account_id, puppet_account_id):
    # get the bootstrapper values from the environment variables
    puppet_account_access_role = os.environ.get("PUPPET_ACCOUNT_ACCESS_ROLE")
    bootstrapper_project_name = os.environ.get("BOOTSTRAPPER_PROJECT_NAME")

    # build the ARN for the assumable role in the Puppet account
    puppet_account_access_role_arn = "arn:aws-us-gov:iam::{}:role/{}".format(
        puppet_account_id, puppet_account_access_role
    )

    logger.info(f"Getting parameters for bootstrapping")
    # use the SSM client in the Puppet account with the assumable role
    with betterboto_client.CrossAccountClientContextManager(
        "ssm", puppet_account_access_role_arn, "assumable_org_role"
    ) as ssm:
        # get the puppet version, role name and path and assumable role in the root account from SSM
        puppet_version = (
            ssm.get_parameter(Name="service-catalog-puppet-version")
            .get("Parameter")
            .get("Value")
        )
        puppet_role_name = (
            ssm.get_parameter(Name="/servicecatalog-puppet/puppet-role/name")
            .get("Parameter")
            .get("Value")
        )
        puppet_role_path = (
            ssm.get_parameter(Name="/servicecatalog-puppet/puppet-role/path")
            .get("Parameter")
            .get("Value")
        )
        assumable_role_in_root_account = (
            ssm.get_parameter(
                Name="/governance-at-scale-account-factory/account-bootstrap-shared-org-bootstrap/AssumableRoleArnInRootAccountForBootstrapping"
            )
            .get("Parameter")
            .get("Value")
        )

    # build the ARN for the assumable role in the member account
    organization_account_access_role_arn = "arn:aws-us-gov:iam::{}:role/{}".format(
        account_id, organization_account_access_role
    )

    with betterboto_client.CrossAccountClientContextManager(
        "codebuild", puppet_account_access_role_arn, "assumable_org_role"
    ) as codebuild:
        logger.info(f"Bootstrapping account {account_id}")
        bootstrapper_build = codebuild.start_build_and_wait_for_completion(
            projectName=bootstrapper_project_name,
            environmentVariablesOverride=[
                {
                    "name": "ASSUMABLE_ROLE_IN_ROOT_ACCOUNT",
                    "value": assumable_role_in_root_account,
                    "type": "PLAINTEXT",
                },
                {
                    "name": "VERSION",
                    "value": puppet_version,
                    "type": "PLAINTEXT",
                },
                {
                    "name": "PUPPET_ACCOUNT_ID",
                    "value": puppet_account_id,
                    "type": "PLAINTEXT",
                },
                {
                    "name": "ORGANIZATION_ACCOUNT_ACCESS_ROLE_ARN",
                    "value": organization_account_access_role_arn,
                    "type": "PLAINTEXT",
                },
                {
                    "name": "PUPPET_ROLE_NAME",
                    "value": puppet_role_name,
                    "type": "PLAINTEXT",
                },
                {
                    "name": "PUPPET_ROLE_PATH",
                    "value": puppet_role_path,
                    "type": "PLAINTEXT",
                },
            ],
        )
        final_status = bootstrapper_build.get("buildStatus")

        if final_status == "SUCCEEDED":
            logger.info(f"Bootstrapping account {account_id}")
            puppet_run_build = codebuild.start_build(
                projectName="servicecatalog-puppet-single-account-run",
                environmentVariablesOverride=[
                    {
                        "name": "SINGLE_ACCOUNT_ID",
                        "value": account_id,
                        "type": "PLAINTEXT",
                    },
                ],
            )
        else:
            logger.error(
                "Errored, check the logs: {}".format(
                    bootstrapper_build.get("logs").get("deepLink")
                )
            )