# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3
import os, logging, json
from crhelper import CfnResource
from botocore.exceptions import ClientError

# declare helper and logging
helper = CfnResource()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# get env variables
S3BucketArn = os.environ['S3BucketARN']
S3BucketName = os.environ['S3BucketName']
region = os.environ['Region']

def lambda_handler(event, context):
    logger.info(event)
    try:
        # Decides whether event is a Customer Resource or an Event Rule
        if event.get('RequestType'):
            helper(event=event, context=context)
        else:
            store_ssm_parameters(event=event, context=context)

    except Exception as e:
        logger.error(e.response)
        raise ValueError(e.response)
            

@helper.create
@helper.update
def store_ssm_parameters(event, context):
    # if event['RequestType'] == 'Delete':
    #     do_nada()
    # else:
    #get region
    # declare boto3 client for ssm
    ssm = boto3.client('ssm', region_name=region)
    # 1. get list of ssm parameters
    parameters = get_ssm_params(event, ssm)
    # 2. get parameter values 
    params_with_values = get_parameter_values(parameters, ssm)
    # 3. store parameters as json objects in s3
    store_params(params_with_values, region)

def get_ssm_params(event, ssm):

    try:
        # get parameters from ssm w/ describe. if too many parameters, 
        # a next token is provided to loop until end
        token_exist = False
        
        parameters = ssm.describe_parameters()
        just_parameters = parameters['Parameters']
        logger.info(parameters)
        
        # print the logs for viewing ssm parameters
        logger.info('The following are ssm parameters collected:')
        logger.info(just_parameters)
        
        if 'NextToken' in parameters:
            token_exist = True
            logger.info('there are more paramters to get.')
            token = parameters['NextToken']
        
        while token_exist:
            logger.info('found next token.')
            next_parameters = ssm.describe_parameters(NextToken = token)
            logger.info(next_parameters)
            just_next_parameters = next_parameters['Parameters']
            # append the lists
            #new_param_dict = {**just_parameters, **just_next_parameters}
            for i in just_next_parameters:
                logger.info(i)
                just_parameters.append(i)
            logger.info(just_parameters)
            #just_parameters = new_param_dict
            
            if 'NextToken' in next_parameters:
                logger.info('But wait, theres more parameters!!!')
                token = next_parameters['NextToken']
            else:
                token_exist = False
        
        return just_parameters

    except ClientError as ex:
        logger.info(ex.response)



def store_params(parameters, region):
    
    # decalare s3 boto3 resource
    s3 = boto3.resource('s3', region_name=region)

    try:
        for parameter in parameters:
            logger.info('uploading parameter to s3')
            logger.info(parameter['Name'])
            logger.info(parameter)
            name = parameter['Name']
            processed_parameter = json_processing(parameter)
            new_object = s3.Object(S3BucketName, str(f'{name}.txt'))
            new_object.put(Body=processed_parameter, BucketKeyEnabled=True)
        
    except ClientError as e:
        logger.info(e.response)

def json_processing(parameter):
    try:
        object = parameter
        #alter data type from datetime to string
        date = str(object['LastModifiedDate'])
        object['LastModifiedDate'] = date
        str_object = json.dumps(object)
        return str_object
    
    except ClientError as ep:
        logger.info(ep.response)   
    

def get_parameter_values(parameters, ssm):
    for param in parameters:
        response = ssm.get_parameter(
           Name = param['Name'],
           WithDecryption = True
        )
        param['Value'] = response['Parameter']['Value']
    return parameters


@helper.delete
def delete_resource(event, context):
    request = event.get('RequestType')
    logger.info(f'received request to remove Custom Resource: {request}, not deleting parameters!')

    