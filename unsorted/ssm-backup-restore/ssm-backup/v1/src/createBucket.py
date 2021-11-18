# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3
import os, logging, json

from botocore.retries import bucket
#from pkg_resources import Version
from crhelper import CfnResource
from botocore.exceptions import ClientError

# declare helper and logging
helper = CfnResource()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# get env variables
DrRegion = os.environ['DrRegion']
S3BucketName = os.environ['S3BucketName']
OriginalLambdaRoleName = os.environ['OriginalLambdaRoleName']
OriginalPolicyName = os.environ['OriginalPolicyName']

def lambda_handler(event, context):
    helper(event, context)

@helper.create
@helper.update
def create_resources(event, context):

    s3 = boto3.client('s3', region_name = DrRegion)
    account_id = event['ResourceProperties']['AccountID']

    #format bucket name
    dr_bucket_name = str(f'disasterrecovery-{S3BucketName}')

    #Create S3 bucket for DR
    response = create_bucket(s3, dr_bucket_name, DrRegion)
    logger.info(f'response from bucket creation{response}')

    #enable bucket versioning
    response = enable_bucket_versioning(s3, dr_bucket_name)
    logger.info(f'response to setting bucket versioning: {response}')

    bucket_arn = str(f'arn:aws:s3:::{dr_bucket_name}')
    helper.Data['bucket_arn'] = bucket_arn

def create_bucket(s3, dr_bucket_name, DrRegion):
    try:
      response = s3.create_bucket(
        Bucket = dr_bucket_name,
        CreateBucketConfiguration = {
          'LocationConstraint': DrRegion
        }
      )
      return response
    except ClientError as e:
      logger.info(e.response)

def enable_bucket_versioning(s3, dr_bucket_name):
  try: 
    response = s3.put_bucket_versioning(
      Bucket = dr_bucket_name,
      VersioningConfiguration={
          'Status': 'Enabled'
        }
      )
    return response
  except ClientError as e:
    logger.info(e.response)

@helper.delete
def delete_bucket(event,context):
    try:
        bucket_name = str(f'disasterrecovery-{S3BucketName}')
        s3_resource = boto3.resource('s3', region_name = DrRegion)
        s3 = boto3.client('s3', region_name = DrRegion)
        bucket = s3_resource.Bucket(bucket_name)
        #Delete bucket objects 1st
        logger.info(f'Deleting bucket objects from bucket:{bucket_name}')
        bucket.objects.all().delete()
        logger.info(f'objects deleted successfully from bucket:{bucket_name}')
        #Delete bucket 2nd
        logger.info(f'Deleting s3 bucket {bucket_name}')
        response = s3.delete_bucket(
            Bucket = bucket_name)
        logger.info(response)
        logger.info(f'deleted s3 bucket {bucket_name}')
        
        return response
    except ClientError as e:
        logger.info(e.response)
        
        