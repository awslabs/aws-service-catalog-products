# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, logging, time
from urllib.request import Request, urlopen
from betterboto import client as betterboto_client
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    request_type = event['RequestType']
    try:
        logger.info(request_type)
        if request_type == 'Create':
            email = event.get('ResourceProperties').get('Email')
            account_name = event.get('ResourceProperties').get('AccountName')
            organization_account_access_role = event.get('ResourceProperties').get('OrganizationAccountAccessRole')
            iam_user_access_to_billing = event.get('ResourceProperties').get('IamUserAccessToBilling')
            target_ou = event.get('ResourceProperties').get('TargetOU')
            assumable_role_in_root_account_arn = os.environ.get('ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN')

            with betterboto_client.CrossAccountClientContextManager(
                    'organizations', assumable_role_in_root_account_arn, 'assumable_org_role'
            ) as organizations:
                logger.info('Creating')
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
                    if target_ou != "None":
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
                    send_response(
                        event,
                        context,
                        "SUCCESS",
                        {
                            "Message": "Resource creation successful!",
                            "account_id": account_id,
                        }
                    )
                else:
                    logger.error(response.get('CreateAccountStatus').get('FailureReason'))
                    send_response(
                        event,
                        context,
                        "FAILED",
                        {
                            "Message": response.get('CreateAccountStatus').get('FailureReason'),
                        }
                    )

        elif request_type == 'Update':
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
