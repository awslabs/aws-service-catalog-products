#!/usr/bin/env python

""" Lambda Function For Putting Metrics into CloudWatch """
from datetime import datetime
import json
import logging
import os

import boto3

# Instantiate the cloud watch client
client = boto3.client('cloudwatch')

# Configure logging
LOGGER = logging.getLogger(__name__)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'true')
if DEBUG_MODE == 'true':
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)


# Configure the metric names for Success, Failure and Cancelled executions
def succeeded_executions():
    return "SucceededExecutions"


def failed_executions():
    return "FailedExecutions"


def cancelled_executions():
    return "CancelledExecutions"


# dictionary for the metric names
pipeline_state_map = {
    'SUCCEEDED': succeeded_executions(),
    'FAILED': failed_executions(),
    'CANCELED': cancelled_executions()
}


def handler(event, context):
    pipeline_name, pipeline_state, execution_timestamp = get_event_info(event)
    put_metrics(pipeline_name, pipeline_state_map[pipeline_state], execution_timestamp)


def get_event_info(event):
    LOGGER.info('Event: {}'.format(json_dump_format(event)))
    pipeline_name = event['detail']['pipeline']
    pipeline_state = event['detail']['state']
    execution_timestamp = event['time']
    return pipeline_name, pipeline_state, execution_timestamp


def put_metrics(name, status, timestamp):
    datetime_obj = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

    client.put_metric_data(
        Namespace='Service Catalog Foundation',
        MetricData=[
            {
                'MetricName': '{}'.format(status),
                'Dimensions': [
                    {
                        'Name': 'By Pipelines',
                        'Value': name
                    }
                ],
                'Timestamp': datetime_obj.timestamp(),
                'Value': 1,
                'Unit': 'Count',
                'StorageResolution': 1
            }
        ]
    )


def json_dump_format(obj):
    return json.dumps(obj, indent=4, sort_keys=True, default=str)
