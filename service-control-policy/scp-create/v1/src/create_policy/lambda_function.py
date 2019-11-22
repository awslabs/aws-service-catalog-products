# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import json
import boto3
import cfnresponse

# Configure logging
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
if len(logging.getLogger().handlers) > 0:
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(format=FORMAT, level=logging.INFO)

def lambda_handler(event, context):
    """ Lambda Function for command execution """
    logging.info("Received event: " + json.dumps(event, indent=2))
    request_type = event['RequestType']
    if request_type == 'Create':
        create_policy(event, context)
    elif request_type == 'Delete':
        delete_policy(event, context)
    elif request_type == 'Update':
        update_policy(event, context)


def get_policy(event):
    s3_bucket = event['ResourceProperties']['S3Bucket']
    s3_object = event['ResourceProperties']['S3Object']
    s3 = boto3.resource('s3')
    policy_file = s3.Object(s3_bucket, s3_object)
    return policy_file.get()['Body'].read().decode('utf-8')


def assume_role(arn, session_name):
    """aws sts assume-role --role-arn arn:aws:iam::00000000000000:role/example-role --role-session-name example-role"""

    sts_client = boto3.client('sts')
    sts_client.get_caller_identity()["Account"]

    response = sts_client.assume_role(
        RoleArn=arn, RoleSessionName=session_name)

    session = boto3.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                            aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                            aws_session_token=response['Credentials']['SessionToken'])

    return session


def create_policy(event, context):
    status = cfnresponse.FAILED
    data = {}
    org_role = event['ResourceProperties']['OrgRole']
    policy_name = event['ResourceProperties']['PolicyName']
    policy_description = event['ResourceProperties']['PolicyDescription']
    policy_id = None

    try:
        session = assume_role(org_role, "CreatePolicy")
        client = session.client('organizations')
        response = client.create_policy(
            Content=get_policy(event),
            Description=policy_description,
            Name=policy_name,
            Type="SERVICE_CONTROL_POLICY"
        )
        policy_id = response['Policy']['PolicySummary']['Id']
        logging.info("Policy created. Policy Id {0}".format(policy_id))
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        logging.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=policy_id)


def update_policy(event, context):
    status = cfnresponse.FAILED
    data = {}
    org_role = event['ResourceProperties']['OrgRole']
    policy_name = event['ResourceProperties']['PolicyName']
    policy_description = event['ResourceProperties']['PolicyDescription']

    try:
        policy_id = event['PhysicalResourceId']
        session = assume_role(org_role, "UpdatePolicy")
        client = session.client('organizations')

        response = client.update_policy(
            Content=get_policy(event),
            Description=policy_description,
            Name=policy_name,
            PolicyId=policy_id
        )

        policy_id = response['Policy']['PolicySummary']['Id']
        logging.info("Policy Updated. Policy Id {0}".format(policy_id))
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        logging.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=policy_id)


def delete_policy(event, context):
    status = cfnresponse.FAILED
    data = {}
    org_role = event['ResourceProperties']['OrgRole']

    try:
        policy_id = event['PhysicalResourceId']
        session = assume_role(org_role, "DeletePolicy")
        client = session.client('organizations')

        response = client.delete_policy(
            PolicyId=policy_id
        )
        logging.debug(response)
        logging.info("Policy {0} deleted.".format(policy_id))
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        logging.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=policy_id)
