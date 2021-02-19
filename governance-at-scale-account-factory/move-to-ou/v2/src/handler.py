# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, logging
from urllib.request import Request, urlopen
from betterboto import client as betterboto_client
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    request_type = event["RequestType"]
    try:
        logger.info(request_type)

        assumable_role_in_root_account_arn = os.environ.get(
            "ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN"
        )
        with betterboto_client.CrossAccountClientContextManager(
                "organizations", assumable_role_in_root_account_arn, "assumable_org_role"
        ) as organizations:
            if request_type in ["Create", "Update"]:
                target_ou = event.get("ResourceProperties").get("TargetOU")
                account_id = event.get("ResourceProperties").get("AccountId")

                result = organizations.list_parents_single_page(ChildId=account_id)
                if len(result.get("Parents", [])) != 1:
                    raise Exception(
                        f"There were unexpected parents for the account_id {account_id}: {json.dumps(result)}"
                    )
                current_ou = result.get("Parents")[0].get('Id')
                if current_ou == target_ou:
                    logger.info("Nothing to do")
                    send_response(
                        event,
                        context,
                        "SUCCESS",
                        {
                            "Message": f"Left in {current_ou}",
                            "account_id": account_id,
                        },
                    )

                elif str(target_ou) != "None" and current_ou != target_ou:
                    logger.info("Moving account to new OU")
                    response = organizations.list_roots()
                    if len(response.get("Roots")) != 1:
                        raise Exception("nRoots: {}".format(len(response.get("Roots"))))
                    if str(target_ou).startswith("/"):
                        target = organizations.convert_path_to_ou(target_ou)
                    else:
                        target = target_ou
                    organizations.move_account(
                        AccountId=account_id,
                        SourceParentId=current_ou,
                        DestinationParentId=target,
                    )

                    send_response(
                        event,
                        context,
                        "SUCCESS",
                        {
                            "Message": f"Moved to {target}",
                            "account_id": account_id,
                        },
                    )

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
