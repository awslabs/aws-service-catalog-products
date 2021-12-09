import boto3
from botocore.exceptions import ClientError
import logging
from crhelper import CfnResource
import os

helper = CfnResource()

# define logging
log = logging.getLogger(__name__)
# define variables
ServiceId = os.environ['ServiceId']


@helper.create
@helper.update

def addpermissiontoendpoint(ServiceId,AccountId):
    try:
        client = boto3.client('ec2')
        log.info(f'Account Id is {AccountId}')
        Principal = 'arn:aws:iam::'+AccountId+':root'
        log.info(f'Principal is {Principal}')
        log.info(f'Adding permission for {Principal} to {ServiceId}')
        response = client.modify_vpc_endpoint_service_permissions(
            DryRun=False,
            ServiceId=ServiceId,
            AddAllowedPrincipals=[
                Principal
            ]
        )
    except ClientError as e:
        log.error(f'Error adding permission for account id {AccountId} to VPC Service Endpoint {ServiceId}')
        log.error(str(e))

def lambda_handler(event,context):
    try:
        AccountId = event['ResourceProperties']['AccountId']
        print(event)
        addpermissiontoendpoint(ServiceId,AccountId)
    except Exception as err:
        log.error('Error encountered')
        log.error(err)
