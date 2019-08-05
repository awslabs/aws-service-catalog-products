#!/usr/bin/env python

""" CodeBuild CloudFormation Lambda Function For Fetching Metrics """
import json
import logging
import os

import boto3

# Instantiate the code build client
client = boto3.client('codebuild')

# Configure logging
LOGGER = logging.getLogger(__name__)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'true')
if DEBUG_MODE == 'true':
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)

# Constants
SUCCESS = "SUCCESS"
FAILED = "FAILED"


def start_build(project_name):
    if not project_name:
        raise ValueError(
            'missing ProjectName resource property'
        )

    response = client.start_build(
        projectName=project_name
    )
    return response


def lambda_handler(event, context):
    LOGGER.info('event: {}'.format(json_dump_format(event)))

    project_name = event.get('ProjectName')

    try:
        start_build_response = start_build(project_name)
        LOGGER.info(
            'start_build response: {}'.format(json_dump_format(start_build_response)
                                              )
        )
        # only return specific fields to prevent "response object is too long" errors
        response = {
            'build_id': start_build_response['build']['id'],
            'project_name': start_build_response['build']['projectName'],
            'arn': start_build_response['build']['arn'],
        }
        response_status = SUCCESS
        request_id = start_build_response['ResponseMetadata']['RequestId']
        reason = 'Create'
    except Exception as e:
        error = 'failed to start build: {}'.format(e)
        LOGGER.error(error)
        response_status = FAILED
        reason = error
        pass

    response_body = {
        'Status': response_status,
        'Reason': ('Reason: ' + json_dump_format(reason) +
                   '. See the details in CloudWatch Log Stream: ' + context.log_stream_name),
        'RequestId': request_id,
        'Data': response
    }

    LOGGER.info(
        'lambda response: {}'.format(json_dump_format(response_body)
                                     )
    )


def json_dump_format(obj):
    return json.dumps(obj, indent=4, sort_keys=True, default=str)
