# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, logging, time
from urllib.request import Request, urlopen
from betterboto import client as betterboto_client
import os
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    request_type = event['RequestType']
    try:
        logger.info(request_type)

        assumable_role_in_root_account_arn = os.environ.get('ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN')
        organization_account_access_role = os.environ.get('ORGANIZATION_ACCOUNT_ACCESS_ROLE')

        with betterboto_client.CrossAccountClientContextManager(
                'organizations', assumable_role_in_root_account_arn, 'assumable_org_role'
        ) as organizations:
            target_ou = event.get('ResourceProperties').get('TargetOU')
            account_name = event.get('ResourceProperties').get('AccountName')
            if request_type == 'Create':
                email = event.get('ResourceProperties').get('Email')
                iam_user_access_to_billing = event.get('ResourceProperties').get('IamUserAccessToBilling')

                account_id = ensure_account_created(
                    organizations,
                    account_name,
                    email,
                    iam_user_access_to_billing,
                    assumable_role_in_root_account_arn,
                    organization_account_access_role,
                )

                ensure_account_is_in_correct_ou(
                    organizations, account_id, target_ou
                )

                send_response(
                    event,
                    context,
                    "SUCCESS",
                    {
                        "Message": "Resource creation successful!",
                        "account_id": account_id,
                    }
                )

            elif request_type == 'Update':
                response = organizations.list_accounts_single_page()
                account_id = None
                for account in response.get('Accounts', []):
                    if account.get('Name') == account_name:
                        account_id = account.get('Id')
                        logger.info('Already created')
                        break
                if account_id is None:
                    raise Exception("Account does not exist")

                ensure_account_is_in_correct_ou(
                    organizations, account_id, target_ou
                )
                send_response(event, context, "SUCCESS",
                              {"Message": "Updated"})
            elif request_type == 'Delete':
                send_response(event, context, "SUCCESS",
                              {"Message": "Deleted"})
            else:
                send_response(event, context, "FAILED",
                              {"Message": "Unexpected"})
    except Exception as ex:
        logger.error(ex)
        send_response(
            event,
            context,
            "FAILED",
            {
                "Message": "Exception"
            }
        )


def ensure_account_is_in_correct_ou(organizations, account_id, target_ou):
    result = organizations.list_parents_single_page(ChildId=account_id)
    current_ou = None
    if len(result.get('Parents', [])) != 1:
        raise Exception(
            f"There were unexpected parents for the account_id {account_id}: {json.dumps(result)}"
        )
        current_ou = result.get('Parents')[1]
    if target_ou != "None":
        if current_ou and current_ou != target_ou:
            logger.info("Moving account to new OU")
            response = organizations.list_roots()
            if len(response.get('Roots')) != 1:
                raise Exception("nRoots: {}".format(len(response.get('Roots'))))
            if str(target_ou).startswith('/'):
                target = organizations.convert_path_to_ou(target_ou)
            else:
                target = target_ou
            organizations.move_account(
                AccountId=account_id,
                SourceParentId=response.get('Roots')[0].get('Id'),
                DestinationParentId=target
            )


def ensure_account_created(
        organizations,
        account_name,
        email,
        iam_user_access_to_billing,
        assumable_role_in_root_account_arn,
        organization_account_access_role,
):
    logger.info('Checking if need to create')
    response = organizations.list_accounts_single_page()
    account_id = None
    for account in response.get('Accounts', []):
        if account.get('Name') == account_name:
            account_id = account.get('Id')
            logger.info('Already created')
            break
    if account_id is None:
        logger.info('Creating account')
        response = organizations.create_account(
            Email=email,
            AccountName=account_name,
            RoleName=organization_account_access_role,
            IamUserAccessToBilling=iam_user_access_to_billing
        )
        id = response.get('CreateAccountStatus').get('Id')
        logger.info('Waiting')
        while response.get('CreateAccountStatus').get('State') == 'IN_PROGRESS':
            logger.info(
                'Still waiting: {}'.format(response.get('CreateAccountStatus').get('State'))
            )
            time.sleep(5)
            response = organizations.describe_create_account_status(CreateAccountRequestId=id)
        logger.info(
            'Finished: {}'.format(response.get('CreateAccountStatus').get('State'))
        )
        if response.get('CreateAccountStatus').get('State') == 'SUCCEEDED':
            account_id = response.get('CreateAccountStatus').get('AccountId')
            counter = 20
            while counter > 0:
                time.sleep(10)
                try:
                    with betterboto_client.CrossMultipleAccountsClientContextManager(
                        'codebuild',
                        [
                            (assumable_role_in_root_account_arn, 'assumable_role_in_root_account_arn'),
                            (f"arn:aws:iam::{account_id}:role/{organization_account_access_role}", 'organization_account_access_role'),
                        ]
                    ) as spoke_codebuild:
                        spoke_codebuild.list_projects()
                        logger.info("Was able to assume role into the spoke and call codebuild")
                        counter = 0
                except Exception as e:
                    counter -= 1
                    logger.error("type error: " + str(e))
                    logger.error(traceback.format_exc())
        else:
            raise Exception(
                f"Account was not created correctly: {response.get('CreateAccountStatus').get('FailureReason')}")
    return account_id


def send_response(e, c, rs, rd):
    r = json.dumps({
        "Status": rs,
        "Reason": "CloudWatch Log Stream: " + c.log_stream_name,
        "PhysicalResourceId": c.log_stream_name,
        "StackId": e['StackId'],
        "RequestId": e['RequestId'],
        "LogicalResourceId": e['LogicalResourceId'],
        "Data": rd
    })
    d = str.encode(r)
    h = {
        'content-type': '',
        'content-length': str(len(d))
    }
    req = Request(e['ResponseURL'], data=d, method='PUT', headers=h)
    r = urlopen(req)
    logger.info("Status message: {} {}".format(r.msg, r.getcode()))
