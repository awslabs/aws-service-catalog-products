# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import logging
import json
import os
from crhelper import CfnResource
import boto3

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL', sleep_on_delete=120, ssl_verify=None)


@helper.create
@helper.update
def create(event, context):
    properties = event.get("ResourceProperties")
    input = dict(
        AccountCreationMethod=properties.get("AccountCreationMethod"),
        ShouldWaitForAccountSubscriptionCreateComplete=properties.get("ShouldWaitForAccountSubscriptionCreateComplete") == 'true',
        ShouldBootstrapAccount=properties.get("ShouldBootstrapAccount") == 'true',
        ShouldRunSingleAccountPipeline=properties.get("ShouldRunSingleAccountPipeline") == 'true',
        ShouldNotifiyOnCompletion=properties.get("ShouldNotifiyOnCompletion") == 'true',
    )

    if properties.get("AccountCreationMethod") == "AWSOrganizations":
        input.update(dict(
            Email=properties.get("Email"),
            AccountName=properties.get("AccountName"),
            RoleName=properties.get("RoleName"),
            IamUserAccessToBilling=properties.get("IamUserAccessToBilling"),
            TargetOrganizationalUnitId=properties.get("TargetOrganizationalUnitId"),
        ))

    elif properties.get("AccountCreationMethod") == "AWSControlTower":
        input.update(dict(
            AccountName=properties.get("AccountName"),
            AccountEmail=properties.get("AccountEmail"),
            SSOUserFirstName=properties.get("SSOUserFirstName"),
            SSOUserLastName=properties.get("SSOUserLastName"),
            SSOUserEmail=properties.get("SSOUserEmail"),
            ManagedOrganizationalUnit=properties.get("ManagedOrganizationalUnit"),
        ))

    state_machine_arn = os.environ.get("STATE_MACHINE_ARN")

    client = boto3.client('stepfunctions')
    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        name=event.get("RequestId"),
        input=json.dumps(input),
    )
    execution_arn = response.get("executionArn")
    helper.Data['execution_arn'] = execution_arn
    return execution_arn


@helper.poll_create
@helper.poll_update
def poll_create(event, context):
    execution_arn = helper.Data['execution_arn']
    client = boto3.client('stepfunctions')
    response = client.describe_execution(executionArn=execution_arn)
    if response.get("status") == "RUNNING":
        return None
    elif response.get("status") in ['FAILED', 'TIMED_OUT', 'ABORTED']:
        raise ValueError(f'Execution {response.get("name")} has finished with status: {response.get("status")}')
    elif response.get("status") == "SUCCEEDED":
        execution_output = json.loads(response.get("output"))
        created_account_id = execution_output.get("CheckAccountOutput").get("account_id")
        return created_account_id
    else:
        raise ValueError(f'Execution {response.get("name")} has finished with unknown status: {response.get("status")}')


def handle(event, context):
    helper(event, context)
