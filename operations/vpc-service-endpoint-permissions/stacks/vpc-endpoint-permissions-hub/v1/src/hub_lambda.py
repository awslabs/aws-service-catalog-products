import boto3
from botocore.exceptions import ClientError
import logging
import traceback
import os
import json

# define logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format='%(levelname)s %(threadName)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO
)


def handle_response_status_and_msg(response):
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        response['responseStatus'] = 'SUCCESS'
    else:
        response['responseStatus'] = 'FAILED'
    response['statusCode'] = response['ResponseMetadata']['HTTPStatusCode']
    return response


def handle_error(event, error_message, statusCode, response_status):
    logger.error(error_message, exc_info=1)
    return {
        'event': event,
        'statusCode': 400,
        'responseStatus': 'FAILED',
        'body': json.dumps(str(error_message))
    }


def add_permission(boto3_session, event, service_id, account_id):
    """
    Adds permission to the VPC Endpoint Service
    """
    logger.info(f'Adding permision to a VPC Endpoint Service')
    response = []
    try:
        Principal = 'arn:aws:iam::' + account_id + ':root'
        logger.info(f'Principal is {Principal}')
        logger.info(f'Adding permission for {Principal} to {service_id}')
        client = boto3_session.client('ec2')
        response = client.modify_vpc_endpoint_service_permissions(
            DryRun=False,
            ServiceId=service_id,
            AddAllowedPrincipals=[
                Principal
            ]
        )
        # example response:
        # {'ReturnValue': True, 'ResponseMetadata': {'RequestId': '1246566a-3ca9-4a87-a8f3-6e098e6171b1', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '1246566a-3ca9-4a87-a8f3-6e098e6171b1', 'cache-control': 'no-cache, no-store', 'strict-transport-security': 'max-age=31536000; includeSubDomains', 'vary': 'accept-encoding', 'content-type': 'text/xml;charset=UTF-8', 'transfer-encoding': 'chunked', 'date': 'Fri, 10 Dec 2021 15:10:46 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}
        # see: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
        response = handle_response_status_and_msg(response)
        logger.info(response)
        return response
    except ClientError as e:
        error_message = f'Error adding permission for account id {account_id} to VPC Service Endpoint {service_id}:\n{str(e)}'
        return handle_error(event, error_message, 400, 'FAILED')


def delete_permission(boto3_session, event, service_id, account_id):
    """
    Deletes permission to the VPC Endpoint Service
    """
    logger.info(f'Deleting permision in a VPC Endpoint Service')
    response = []
    try:
        Principal = 'arn:aws:iam::'+ account_id +':root'
        logger.info(f'Principal is {Principal}')
        logger.info(f'Deleting permission for {Principal} in {service_id}')
        client = boto3_session.client('ec2')
        response = client.modify_vpc_endpoint_service_permissions(
            DryRun=False,
            ServiceId=service_id,
            RemoveAllowedPrincipals=[
                Principal
            ]
        )
        response = handle_response_status_and_msg(response)
        logger.info(response)
        return response
    except ClientError as e:
        error_message = f'Error deleting permission for account id {account_id} to VPC Service Endpoint {service_id}:\n{str(e)}'
        return handle_error(event, error_message, 400, 'FAILED')


def update_permission(boto3_session, event, service_id, old_account_id, new_account_id):
    logger.info(f'Updating permision in a VPC Endpoint Service')
    response = delete_permission(boto3_session, event, service_id, old_account_id)

    if response['responseStatus'] == 'SUCCESS':
        response = add_permission(boto3_session, event, service_id, new_account_id)
        return response
    else:
        # do not run the 2nd API call when the 1st call failed
        return response


def get_current_account_id():
    client = boto3.client('sts')
    account_id = client.get_caller_identity()["Account"]
    return account_id


def get_boto3_session(role_arn_in_networking_account):
    current_account_id = get_current_account_id()

    try:
        networking_account_id = int(role_arn_in_networking_account.split(':')[4])
    except Exception as e:
        networking_account_id = current_account_id
        logger.warning(f'Invalid IAM Role ARN set {role_arn_in_networking_account}, therefore we will not assume this role')
        logger.error(traceback.format_exc())

    if current_account_id != networking_account_id:
        logger.info(f'Assuming role {role_arn_in_networking_account} in the networking AWS Account {networking_account_id}')
        sts = boto3.client('sts')
        token = sts.assume_role(
            RoleArn = role_arn_in_networking_account,
            RoleSessionName ='VPCEndpointPermissions')
        cred = token['Credentials']
        temp_access_key = cred['AccessKeyId']
        temp_secret_key = cred['SecretAccessKey']
        session_token = cred['SessionToken']

        session = boto3.session.Session(
            aws_access_key_id=temp_access_key,
            aws_secret_access_key=temp_secret_key,
            aws_session_token=session_token
        )
        return session
    return boto3.Session()



def lambda_handler(event, context):
    try:
        logger.info(event)

        # get parameters values
        service_id = os.environ['ServiceId']
        logger.info(f'ServiceId is {service_id}')
        account_id = event['parameters']['AccountId']
        logger.info(f'AccountId for which the permission will be set is {account_id}')
        role_arn_in_networking_account = event['parameters']['RoleARNInNetworkingAccountId']
        logger.info(f'RoleARNInNetworkingAccountId is {role_arn_in_networking_account}')
        action = event['parameters']['RequestType']
        logger.info(f'RequestType is {action}')

        boto3_session = get_boto3_session(role_arn_in_networking_account)

        if action == 'Create':
            response = add_permission(boto3_session, event, service_id, account_id)
        elif action == 'Update':
            old_account_id = event['parameters']['OldAccountId']
            response = update_permission(boto3_session, event, service_id, old_account_id, account_id)
        elif action == 'Delete':
            response = delete_permission(boto3_session, event, service_id, account_id)
        else:
            error_message = f'Unsupported action: {action}'
            return handle_error(event, error_message, 400, 'FAILED')
        return response


    except Exception as err:
        logger.error(traceback.format_exc())
        return handle_error(event, traceback.format_exc(), 500, 'FAILED')
