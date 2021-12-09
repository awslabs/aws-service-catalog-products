import sys
import json
import logging
import threading
import traceback
import os
import boto3
import requests
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format='%(levelname)s %(threadName)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO
)

HUB_ACC_ROLE_ARN = os.environ['VPCE_PERM_ROLE_ARN']
FUNC_NAME = os.environ['FUNC_NAME']

# assume role in other account
sts = boto3.client('sts')
token = sts.assume_role(RoleArn=HUB_ACC_ROLE_ARN, RoleSessionName='VPCE_PERMISSIONS')
cred = token['Credentials']
temp_access_key = cred['AccessKeyId']
temp_secret_key = cred['SecretAccessKey']
session_token = cred['SessionToken']

session = boto3.session.Session(
    aws_access_key_id=temp_access_key,
    aws_secret_access_key=temp_secret_key,
    aws_session_token=session_token
)

client = session.client('lambda')


def create(event, lambda_client):
    """
    Invokes the Lambda in the Networking Account to add permisions to the VPC Endpoint Service
    """
    logger.info("Making CREATE call to Lambda function in NETWORK account to add permission to VPC Endpoint Service")

    try:
        response = lambda_client.invoke(
            FunctionName=FUNC_NAME,
            LogType='Tail',
            Payload=json.dumps(event)
        )
        if "FunctionError" in response.keys():
            raise Exception("Remote invocation error!")
        return

    except ClientError as e:
        msg = "Unable to trigger VPC Endpoint permission Lambda function in NETWORK account"
        logger.error(msg)
        logger.error(str(e))
        raise Exception(msg)

def delete(event, lambda_client):
    """
    Invokes the Lambda in the Networking Account to add permisions to the VPC Endpoint Service
    """
    logger.info("Making CREATE call to Lambda function in NETWORK account to add permission to VPC Endpoint Service")

    try:
        response = lambda_client.invoke(
            FunctionName=FUNC_NAME,
            LogType='Tail',
            Payload=json.dumps(event)
        )
        if "FunctionError" in response.keys():
            raise Exception("Remote invocation error!")
        return

    except ClientError as e:
        msg = "Unable to trigger VPC Endpoint permission Lambda function in NETWORK account"
        logger.error(msg)
        logger.error(str(e))
        raise Exception(msg)

def update(event, lambda_client):
    """
    Invokes the Lambda in the Networking Account to add permisions to the VPC Endpoint Service
    """
    logger.info("Making CREATE call to Lambda function in NETWORK account to add permission to VPC Endpoint Service")

    try:
        response = lambda_client.invoke(
            FunctionName=FUNC_NAME,
            LogType='Tail',
            Payload=json.dumps(event)
        )
        if "FunctionError" in response.keys():
            raise Exception("Remote invocation error!")
        return

    except ClientError as e:
        msg = "Unable to trigger VPC Endpoint permission Lambda function in NETWORK account"
        logger.error(msg)
        logger.error(str(e))
        raise Exception(msg)
        

def send_response(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or event['LogicalResourceId']
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    response = requests.put(responseUrl, data=json_responseBody, headers=headers)
    return
        
def lambda_handler(event,context):
    request_type = 'Create'
    try:
        if request_type == 'Create':
            create(event,client)
            send_response(event, context, "SUCCESS", {"Message": "Created"})
        else:
            send_response(event, context, "FAILED",  {"Message": "Unexpected"})
            
    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        send_response(event, context, "FAILED", {"Message": "Exception"})
        
