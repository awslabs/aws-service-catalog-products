# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3
import os, logging, json, time
from botocore.exceptions import ClientError

# Declare logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get env variables
S3BucketName = os.environ['S3BucketName']
Region = os.environ['Region']
StackName = os.environ['StackName']
SNSTopicARN = os.environ['SNSTopicArn']
MainBucketName = os.environ['MainBucketName']
DRBucketArn = os.environ['DRBucketArn']

def lambda_handler(event, context):
    setup_dr_bucket_policy(event, context)
    restore_ssm_parameters(event, context)

def restore_ssm_parameters(event, context):
    try:
        # Set s3 boto3 client
        s3 = boto3.client('s3')
        # Declare boto3 client for ssm
        ssm = boto3.client('ssm', region_name= Region)
        # List objects in the bucket
        objects = list_parameters_in_bucket(s3)
        params_to_restore = [obj['Key'] for obj in objects]
        # Set s3 resource
        s3_resource = boto3.resource('s3')
        # Get objects
        for o in objects:
            s3_object = get_object(o['Key'],s3_resource)
            logger.info(s3_object)
            response = formulate_parameter(s3_object, ssm)
            logger.info(response)
        # Clean up resources associated with this invocation of restore
        clean_up(params_to_restore)
        
    except ClientError as restore_ssm_error:
        logger.info(restore_ssm_error.response)

def setup_dr_bucket_policy(event, context):
    try:
        s3 = boto3.client('s3')
        response = s3.get_bucket_policy(Bucket=MainBucketName)
        policy = json.loads(response['Policy'])
        policy['Statement'][0]['Resource'] = DRBucketArn
        policy['Statement'][1]['Resource'] = DRBucketArn + "/*"
        bucket_policy = json.dumps(policy)
        response = s3.put_bucket_policy(Bucket=DRBucketArn.split(':::')[1], Policy=bucket_policy)
        return response
    except ClientError as e:
        logger.info(e.response)

def clean_up(params_restored):
    error_status = 0
    try:
        # Set service catalog client
        sc = boto3.client('servicecatalog')
        # Get provisioned product id of 'this' product
        pp_id = StackName[StackName.find('pp-'):]
        # Make sure provisioned product is in the AVAILABLE state
        while True:
            response = sc.describe_provisioned_product(Id=pp_id)
            pp_status = response['ProvisionedProductDetail']['Status']

            if (pp_status == 'AVAILABLE'):
                break
            elif (pp_status == 'ERROR' or pp_status == 'TAINTED'):
                logger.error("Service Catalog Product is in an error state!")
                error_status = ("The Service Catalog product associated with the restoration has entered a bad state.\n"
                "Please have an administrator troubleshoot with the following logs:\n" + response['ProvisionedProductDetail']['StatusMessage'])
                break
            else:
                logger.info("Sleeping for 5 seconds - waiting for Service Catalog Provisioned Product to be AVAILABLE")
                time.sleep(5)
        # Terminate provisoned product
        logger.info("Cleaning up Service Catalog Provisioned Product ...")
        response = sc.terminate_provisioned_product(ProvisionedProductId=pp_id)
        # Determine what message to send
        if error_status:
            message = (error_status + "\nThe Service Catalog Provisioned Product for restoration has been terminated and "
            "the associated CloudFormation Stack has been deleted.")
        else:
            message = ("The SSM Restoration has completed.\nThe Service Catalog Provisioned Product for restoration "
            "has been terminated and the associated CloudFormation Stack has been deleted. The following is a list of " 
            f"restored parameters:\n{params_restored}")
        # Send SNS email that restore is complete
        sns = boto3.client('sns')
        logger.info("SNS Topic being sent ...")
        sns.publish(
            TopicArn = SNSTopicARN,
            Subject = "SSM Restoration Progress",
            Message = message
        )

    except ClientError as clean_up_error:
        logger.info(clean_up_error.response)

def list_parameters_in_bucket(s3):
    try:
        logger.info("getting objects from the S3 bucket...")

        response = s3.list_objects_v2(
            Bucket = S3BucketName
        )

        objects = response['Contents']

        if response['IsTruncated'] == False:
            key_count = response['KeyCount']
            logger.info(f'Got {key_count} keys from the S3 bucket. No more to get')
        else:
            next_continuation_token = response['NextContinuationToken']
            logger.info('got a continuation token, still pulling objects')
            key_count = response['KeyCount']

            more_keys = True

            while more_keys:
                next_response = s3.list_objects_v2(
                    Bucket = S3BucketName,
                    ContinuationToken = next_continuation_token
                )

                next_objects = next_response['Contents']

                for i in next_objects:
                    objects.append(i)
                
                if next_response['IsTruncated'] == False:
                    more_keys = False
                else:
                    next_continuation_token = next_response['NextContinuationToken']
        
        logger.info('got objects from bucket:')
        logger.info(objects)

        return objects
    except ClientError as list_objects_error:
        logger.info(list_objects_error.response)


def get_object(key_name,s3_resource):
    try:
        str_obj = s3_resource.Object(S3BucketName,key_name)
        response = str_obj.get()['Body'].read()
        return response
        
    except ClientError as getObject_error:
        logger.info(getObject_error.response)

def create_parameter(name, value, p_type, tier, data_type, ssm):
    try:
        logger.info('creating parameter')
        response = ssm.put_parameter(
            Name = name,
            Value = value,
            Type = p_type,
            Tier = tier,
            DataType = data_type,
            Overwrite = True
        )
        logger.info(name)
        return response
    except ClientError as create_parameter_error:
        logger.info(create_parameter_error.response) 

def formulate_parameter(object, ssm):
    try:
        json_obj = json.loads(object)
        name = json_obj['Name']
        value = json_obj['Value']
        p_type = json_obj['Type']
        tier = json_obj['Tier']
        data_type = json_obj['DataType']
        response = create_parameter(name, value, p_type, tier, data_type, ssm)

        return response

    except ClientError as formulate_parameter:
        logger.info(formulate_parameter.response)   