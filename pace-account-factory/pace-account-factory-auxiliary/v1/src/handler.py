import os

from crhelper import CfnResource
import logging
from betterboto import client as betterboto_client

logger = logging.getLogger(__name__)

helper = CfnResource(
    json_logging=False,
    log_level='DEBUG',
    boto_level='CRITICAL',
    sleep_on_delete=120,
    ssl_verify=None
)

try:
    ## Init code goes here
    pass
except Exception as e:
    helper.init_failure(e)


@helper.create
def create(event, context):
    logger.info("Got a create request.  Going to create an AWS Account")

    mode = event.get("ResourceProperties").get("Mode")

    if mode == "AWS_ORGANIZATIONS":
        account_creation_role_in_root_account_arn = os.environ.get(
            "ACCOUNT_CREATION_ROLE_IN_ROOT_ACCOUNT_ARN"
        )
        organization_account_access_role_name = event.get("ResourceProperties").get("OrganizationAccountAccessRoleName")

        account_name = event.get("ResourceProperties").get("AccountName")
        email = event.get("ResourceProperties").get("Email")
        iam_user_access_to_billing = event.get("ResourceProperties").get(
            "IamUserAccessToBilling"
        )

        with betterboto_client.CrossAccountClientContextManager(
                "organizations",
                account_creation_role_in_root_account_arn,
                "assumable_org_role",
        ) as organizations:
            logger.info("Creating account")
            response = organizations.create_account(
                Email=email,
                AccountName=account_name,
                RoleName=organization_account_access_role_name,
                IamUserAccessToBilling=iam_user_access_to_billing
            )
            create_account_status_id = response.get("CreateAccountStatus").get("Id")
            helper.Data.update(
                {
                    "create_account_status_id": create_account_status_id,
                    "account_name": account_name,
                }
            )


def account_is_ready_to_be_bootstraped(event, target_account_id):
    organization_account_access_role_name = event.get("ResourceProperties").get("OrganizationAccountAccessRoleName")

    hop1 = (os.environ.get('ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN'), 'assumable_role_in_root_account_arn')
    hop2 = (f'arn:aws:iam::{target_account_id}:role/{organization_account_access_role_name}',
            'assumable_org_role_for_codebuild')
    with betterboto_client.CrossMultipleAccountsClientContextManager(
            'codebuild',
            [hop1, hop2]
    ) as codebuild:
        try:
            result = codebuild.list_projects()
            logger.info(f"Was able to list projects: {result}")
        except Exception as e:
            logger.info(f"Codebuild not available in target account yet: {str(e)}")
            return False
    with betterboto_client.CrossMultipleAccountsClientContextManager(
            "cloudformation",
            [hop1, hop2]
    ) as cloudformation:
        try:
            result = cloudformation.list_stacks()
            logger.info(f"Was able to list stacks: {result}")
            return True
        except Exception as e:
            logger.info(f"Cloudformation not available in target account yet: {str(e)}")
            return False


def get_account_id_for(create_account_status_id, account_name):
    logger.info("Checking if account was created")
    with betterboto_client.CrossAccountClientContextManager(
            "organizations",
            os.environ.get("ACCOUNT_CREATION_ROLE_IN_ROOT_ACCOUNT_ARN"),
            "assumable_org_role",
    ) as organizations:
        create_account_status = organizations.describe_create_account_status(
            CreateAccountRequestId=create_account_status_id
        ).get("CreateAccountStatus")

        state = create_account_status.get("State")
        if state == "IN_PROGRESS":
            return None

        if state == "FAILED":
            logger.info("Account creation failed")
            if str(os.environ.get("ALLOW_RESUMPTION")) == "True" and create_account_status.get( "FailureReason") == "EMAIL_ALREADY_EXISTS":
                pass
            else:
                raise Exception(create_account_status.get("FailureReason"))

        if state == "SUCCEEDED":
            pass

        accounts = organizations.list_accounts_single_page().get("Accounts")
        for acc in accounts:
            if acc.get('Name') == account_name:
                return acc.get("Id")
        raise Exception("Account was created but account name could not be found in the org")


@helper.poll_create
def poll_create(event, context):
    create_account_status_id = event['CrHelperData'].get("create_account_status_id")
    account_name = event['CrHelperData'].get("account_name")

    logger.info(f"Got create poll request.  Checking AWS Account Creation for: {create_account_status_id}")
    account_id = get_account_id_for(create_account_status_id, account_name)

    if account_id is None:
        return None

    account_type = event.get("ResourceProperties").get("AccountType")
    account_group = event.get("ResourceProperties").get("AccountGroup")

    with betterboto_client.ClientContextManager('ssm') as ssm:
        ssm_parameter_name = f"{os.environ.get('SSM_OU_MAP_PREFIX')}/{account_group}/{account_type}"
        logger.info(f"Getting target_ou from ssm: {ssm_parameter_name}")
        target_ou = ssm.get_parameter(Name=ssm_parameter_name).get("Parameter").get("Value")


    with betterboto_client.CrossAccountClientContextManager(
            "organizations",
            os.environ.get("ACCOUNT_CREATION_ROLE_IN_ROOT_ACCOUNT_ARN"),
            "assumable_org_role",
    ) as organizations:
        if str(target_ou).startswith("/"):
            target = organizations.convert_path_to_ou(target_ou)
        else:
            target = target_ou

        result = organizations.list_parents_single_page(ChildId=account_id)
        current_ou = result.get("Parents")[0].get('Id')

        if target != current_ou:
            logger.info(f"Need to move account to: {target}")
            organizations.move_account(
                AccountId=account_id,
                SourceParentId=current_ou,
                DestinationParentId=target,
            )

    account_ready = account_is_ready_to_be_bootstraped(event, account_id)
    logger.info(f"account_ready: {account_ready}")

    if not account_ready:
        return None

    with betterboto_client.ClientContextManager(
            'codebuild',
    ) as codebuild:
        paginator = codebuild.get_paginator('list_builds_for_project')
        for page in paginator.paginate(
            projectName=os.environ.get('BOOTSTRAPPER_PROJECT_NAME'),
        ):



        logger.info("Checking previously started bootstrapping")

            response = codebuild.batch_get_builds(ids=[bootstrap_build_id])
            build = response.get('builds')[0]
            build_status = build.get('buildStatus')
            if build_status == 'SUCCEEDED':
                logger.info("account was bootstrapped correctly")
                helper.Data.update({"account_bootstrapped": True})
            elif build_status == "IN_PROGRESS":
                return None
            else:
                raise Exception(f"Bootstrapping not succeeded: {build_status}")
        else:
            logger.info("Starting bootstrap")
            organization_account_access_role_name = event.get("ResourceProperties").get(
                "OrganizationAccountAccessRoleName")
            organization_account_access_role_arn = 'arn:aws:iam::{}:role/{}'.format(
                target_account_id, organization_account_access_role_name
            )
            response = codebuild.start_build(
                projectName=os.environ.get('BOOTSTRAPPER_PROJECT_NAME'),
                environmentVariablesOverride=[
                    {
                        'name': 'ASSUMABLE_ROLE_IN_ROOT_ACCOUNT',
                        'value': os.environ.get('ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN'),
                        'type': 'PLAINTEXT'
                    },
                    {
                        'name': 'ORGANIZATION_ACCOUNT_ACCESS_ROLE_ARN',
                        'value': organization_account_access_role_arn,
                        'type': 'PLAINTEXT'
                    },
                ],
            )
            build_id = response.get("build").get("id")
            logger.info(f"Bootstrap started: {build_id}")
            helper.Data.update({"bootstrap_build_id": build_id})
            return None

    logger.info(f"account was not inflated")
    with betterboto_client.ClientContextManager(
            'codebuild',
    ) as codebuild:
        if event['CrHelperData'].get("inflate_build_id"):
            logger.info("Checking previously started single account run")
            inflate_build_id = event['CrHelperData'].get("inflate_build_id")
            response = codebuild.batch_get_builds(ids=[inflate_build_id])
            build = response.get('builds')[0]
            build_status = build.get('buildStatus')
            if build_status == 'SUCCEEDED':
                helper.Data.update({"account_inflated": True})
                return target_account_id
            elif build_status == "IN_PROGRESS":
                return None
            else:
                raise Exception(f"Single account run not succeeded: {build_status}")
        else:
            logger.info("Starting single account run")
            response = codebuild.start_build(
                projectName=os.environ.get("SINGLE_ACCOUNT_RUN_PROJECT_NAME"),
                environmentVariablesOverride=[
                    {
                        'name': 'SINGLE_ACCOUNT_ID',
                        'value': target_account_id,
                        'type': 'PLAINTEXT'
                    },
                ]
            )
            helper.Data.update(
                {
                    "inflate_build_id": response.get("build").get("id")
                }
            )
            return None

    return False


@helper.update
def update(event, context):
    logger.info("Got Update")
    # If the update resulted in a new resource being created, return an id for the new resource.
    # CloudFormation will send a delete event with the old id when stack update completes


@helper.poll_update
def poll_update(event, context):
    logger.info("Got update poll")
    # Return a resource id or True to indicate that creation is complete. if True is returned an id
    # will be generated
    return True


@helper.delete
def delete(event, context):
    logger.info("Got Delete")
    # Delete never returns anything. Should not fail if the underlying resources are already deleted.
    # Desired state.


@helper.poll_delete
def poll_delete(event, context):
    logger.info("Got delete poll")
    # Return a resource id or True to indicate that creation is complete. if True is returned an id
    # will be generated
    return True


def handler(event, context):
    helper(event, context)
