# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json, logging, time
from urllib.request import Request, urlopen
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


def handler(event, context):
    request_type = event["RequestType"]
    try:
        logger.info(request_type)
        if request_type == "Create":
            target_account_id = event.get("ResourceProperties").get("TargetAccountId")
            puppet_account_id = event.get("ResourceProperties").get("PuppetAccountId")
            organization_account_access_role_name = event.get("ResourceProperties").get(
                "OrganizationAccountAccessRoleName"
            )
            puppet_account_access_role_name = event.get("ResourceProperties").get(
                "PuppetAccountAccessRoleName"
            )

            partition = event.get("ResourceProperties").get("AccountPartition")

            organization_account_access_role_arn = "arn:{}:iam::{}:role/{}".format(
                partition, target_account_id, organization_account_access_role_name
            )
            puppet_account_access_role_arn = "arn:{}:iam::{}:role/{}".format(
                partition, puppet_account_id, puppet_account_access_role_name
            )

            with betterboto_client.CrossAccountClientContextManager(
                "ssm", puppet_account_access_role_arn, "assumable_org_role"
            ) as ssm:
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
                assumable_role_in_root_account = os.environ.get(
                    "ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN"
                )

            bootstrapper_project_name = os.environ.get("BOOTSTRAPPER_PROJECT_NAME")

            with betterboto_client.CrossAccountClientContextManager(
                "codebuild", puppet_account_access_role_arn, "assumable_org_role"
            ) as codebuild:
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
                    puppet_run_build = codebuild.start_build(
                        projectName="servicecatalog-puppet-single-account-run-with-callback",
                        environmentVariablesOverride=[
                            {
                                "name": "SINGLE_ACCOUNT_ID",
                                "value": target_account_id,
                                "type": "PLAINTEXT",
                            },
                            {
                                "name": "CALLBACK_URL",
                                "value": event.get("ResourceProperties").get("Handle"),
                                "type": "PLAINTEXT",
                            },
                        ],
                    ).get("build")

                    send_response(
                        event,
                        context,
                        "SUCCESS",
                        {
                            "Message": "Resource creation successful!",
                            "puppet_run_build_id": puppet_run_build.get("id"),
                            "bootstrapper_build_id": bootstrapper_build.get("id"),
                        },
                    )
                else:
                    logger.error(
                        "Errored check the logs: {}".format(
                            bootstrapper_build.get("logs").get("deepLink")
                        )
                    )
                    send_response(
                        event,
                        context,
                        "FAILED",
                        {
                            "Message": "Bootstrap errored, check the logs: {}".format(
                                bootstrapper_build.get("logs").get("deepLink")
                            ),
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
        traceback.print_tb(ex.__traceback__)
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
