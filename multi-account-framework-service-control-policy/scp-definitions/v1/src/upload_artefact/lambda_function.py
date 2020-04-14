import os
import glob
import logging
import json
import boto3
import cfnresponse

# Configure logging 
LOGGER = logging.getLogger(__name__)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'true')
if DEBUG_MODE == 'true':
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)

prefix = os.getenv('VERSION')

def lambda_handler(event, context):
    """ Lambda Function for command execution """
    LOGGER.info("Received event: " + json.dumps(event, indent=2))
    print(event)
    request_type = event['RequestType']
    if request_type == 'Create':
        upload_policy(event, context)
    elif request_type == 'Update':
        upload_policy(event, context)
    elif request_type == 'Delete':
        delete_policy(event,context)

def upload_policy(event, context):
    status = cfnresponse.FAILED
    data = {}

    try:
        s3_bucket = event['ResourceProperties']['S3Bucket']
        files = glob.glob("artefacts/*")

        s3 = boto3.resource('s3')

        for file in files:
            s3.Bucket(s3_bucket).upload_file(file, f"{prefix}/{file.split('/')[-1]}")

        status = cfnresponse.SUCCESS

    except BaseException as ex:
        LOGGER.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=None)

def delete_policy(event, context):
    status = cfnresponse.FAILED
    data = {}

    try:
        s3_bucket = event['ResourceProperties']['S3Bucket']

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(s3_bucket)
        resp = bucket.objects.all().delete()
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        LOGGER.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=None)


