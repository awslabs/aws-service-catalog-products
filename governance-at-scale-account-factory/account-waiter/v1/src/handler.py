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
        logger.info(request_type)

        if request_type in ["Create", "Update"]:
            codebuild_project_to_run = os.environ.get("CODEBUILD_PROJECT_TO_RUN")
            assumable_role_in_root_account_arn = os.environ.get(
                "ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN"
            )
            organization_account_access_role = os.environ.get(
                "ORGANIZATION_ACCOUNT_ACCESS_ROLE"
            )

            with betterboto_client.ClientContextManager("codebuild") as codebuild:
                response = codebuild.start_build(
                    projectName=codebuild_project_to_run,
                    environmentVariablesOverride=[
                        {
                            "name": "ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN",
                            "value": assumable_role_in_root_account_arn,
                            "type": "PLAINTEXT",
                        },
                        {
                            "name": "ORGANIZATION_ACCOUNT_ACCESS_ROLE",
                            "value": organization_account_access_role,
                            "type": "PLAINTEXT",
                        },
                        {
                            "name": "RESULTS_URL",
                            "value": event.get("ResourceProperties").get("Handle"),
                            "type": "PLAINTEXT",
                        },
                    ],
                )
                build_status = response.get("build").get("buildStatus")
                send_response(
                    event,
                    context,
                    "SUCCESS",
                    {
                        "Message": f"{request_type} successful.  Build status: {build_status}",
                    },
                )

        else:
            send_response(
                event,
                context,
                "SUCCESS",
                {
                    "Message": f"{request_type} successful",
                },
            )

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
