# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, logging, time
from urllib.request import Request, urlopen
from betterboto import client as betterboto_client
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    request_type = event["RequestType"]
    try:
        logger.info(f"Incomming Event: {event}")
        logger.info(f"Request Type: {request_type}")

        if request_type in ["Create", "Update"]:
            assumable_role_in_root_account_arn = os.environ.get(
                "ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN"
            )
            organization_account_access_role = os.environ.get(
                "ORGANIZATION_ACCOUNT_ACCESS_ROLE"
            )

            partition = event.get("ResourceProperties").get("AccountPartition")
            account_name = event.get("ResourceProperties").get("AccountName")
            email = event.get("ResourceProperties").get("Email")
            iam_user_access_to_billing = event.get("ResourceProperties").get(
                "IamUserAccessToBilling"
            )

            with betterboto_client.CrossAccountClientContextManager(
                "organizations",
                assumable_role_in_root_account_arn,
                "assumable_org_role",
            ) as organizations:
                logger.info("Checking if the account already exists")
                response = organizations.list_accounts_single_page()
                for account in response.get("Accounts", []):
                    if account.get("Name") == account_name:
                        account_id = account.get("Id")
                        logger.info(
                            f"Account {account_name} already exists in Commercial. No further action was taken"
                        )
                        send_response(
                            event,
                            context,
                            "SUCCESS"
                            if account.get("Status") == "ACTIVE"
                            and partition != "GovCloud"
                            else "FAILED",
                            {
                                "Message": f"Account {account_name} already exists in Commercial",
                                "account_id": account_id,
                            },
                        )
                        return

                if partition == "GovCloud":
                    logger.info("Creating the accounts for GovCloud")
                    response = organizations.create_gov_cloud_account(
                        Email=email,
                        AccountName=account_name,
                        RoleName=organization_account_access_role,
                        IamUserAccessToBilling=iam_user_access_to_billing,
                    )
                else:
                    logger.info("Creating the account")
                    response = organizations.create_account(
                        Email=email,
                        AccountName=account_name,
                        RoleName=organization_account_access_role,
                        IamUserAccessToBilling=iam_user_access_to_billing,
                    )

                id = response.get("CreateAccountStatus").get("Id")
                logger.info("Waiting")
                while response.get("CreateAccountStatus").get("State") == "IN_PROGRESS":
                    logger.info(
                        "Still waiting: {}".format(
                            response.get("CreateAccountStatus").get("State")
                        )
                    )
                    time.sleep(5)
                    response = organizations.describe_create_account_status(
                        CreateAccountRequestId=id
                    )
                state = response.get("CreateAccountStatus").get("State")
                account_id = response.get("CreateAccountStatus").get("AccountId")
                govcloud_account_id = response.get("CreateAccountStatus").get(
                    "GovCloudAccountId"
                )
                logger.info(f"Finished: {state}")
                logger.info(f"Response: {response}")
                send_response(
                    event,
                    context,
                    "SUCCESS" if state == "SUCCEEDED" else "FAILED",
                    {
                        "Message": "Account was created"
                        if state == "SUCCEEDED"
                        else f"Failed: {response.get('CreateAccountStatus').get('FailureReason')}",
                        "account_id": account_id,
                        "govcloud_account_id": govcloud_account_id,
                    },
                )

        elif request_type == "Update":
            send_response(event, context, "SUCCESS", {"Message": "Updated"})
        elif request_type == "Delete":
            send_response(event, context, "SUCCESS", {"Message": "Deleted"})
        else:
            send_response(event, context, "FAILED", {"Message": "Unexpected"})
    except Exception as ex:
        logger.error(ex)
        send_response(event, context, "FAILED", {"Message": "Exception"})


def send_response(e, c, rs, rd):
    r = json.dumps(
        {
            "Status": rs,
            "Reason": "CloudWatch Log Stream: " + c.log_stream_name,
            "PhysicalResourceId": c.log_stream_name,
            "StackId": e["StackId"],
            "RequestId": e["RequestId"],
            "LogicalResourceId": e["LogicalResourceId"],
            "Data": rd,
        }
    )
    d = str.encode(r)
    h = {"content-type": "", "content-length": str(len(d))}
    req = Request(e["ResponseURL"], data=d, method="PUT", headers=h)
    r = urlopen(req)
    logger.info("Status message: {} {}".format(r.msg, r.getcode()))
