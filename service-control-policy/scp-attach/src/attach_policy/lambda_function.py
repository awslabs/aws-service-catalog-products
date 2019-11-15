# Any code, applications, scripts, templates, proofs of concept, documentation
# and other items provided by AWS under this SOW are "AWS Content,"" as defined
# in the Agreement, and are provided for illustration purposes only. All such
# AWS Content is provided solely at the option of AWS, and is subject to the
# terms of the Addendum and the Agreement. Customer is solely responsible for
# using, deploying, testing, and supporting any code and applications provided
# by AWS under this SOW.
#
# (c) 2019 Amazon Web Services

import os
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
        attach_policy(event, context)
    elif request_type == 'Delete':
        detach_policy(event, context)
    elif request_type == 'Update':
        update_policy(event, context)


def attach_policy(event, context):
    status = cfnresponse.FAILED
    data = {}

    policy_id = event['ResourceProperties']['PolicyId']
    target_id = event['ResourceProperties']['TargetId']
    org_role = event['ResourceProperties']['OrgRole']

    try:
        session = assume_role(org_role, "AttachPolicy")
        client = session.client('organizations')
        response = client.attach_policy(
            PolicyId=policy_id,
            TargetId=target_id
        )
        logging.info(response)
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        logging.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=None)


def detach_policy(event, context):
    status = cfnresponse.FAILED
    data = {}

    policy_id = event['ResourceProperties']['PolicyId']
    target_id = event['ResourceProperties']['TargetId']
    org_role = event['ResourceProperties']['OrgRole']

    try:
        session = assume_role(org_role, "DetachPolicy")
        client = session.client('organizations')
        response = client.detach_policy(
            PolicyId=policy_id,
            TargetId=target_id
        )
        logging.info(response)
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        logging.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=None)


def update_policy(event, context):
    status = cfnresponse.FAILED
    data = {}
    org_role = event['ResourceProperties']['OrgRole']
    old_policy_id = event['OldResourceProperties']['PolicyId']
    old_target_id = event['OldResourceProperties']['TargetId']

    new_policy_id = event['ResourceProperties']['PolicyId']
    new_target_id = event['ResourceProperties']['TargetId']

    try:
        session = assume_role(org_role, "UpdatePolicy")
        client = session.client('organizations')

        response = client.detach_policy(
            PolicyId=old_policy_id,
            TargetId=old_target_id
        )
        logging.info(response)

        response = client.attach_policy(
            PolicyId=new_policy_id,
            TargetId=new_target_id
        )
        logging.info(response)
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        logging.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=None)


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
