import os
import json
import boto3
from hub_lambda import (
    lambda_handler)


test_vpc_endpoint_service_id = 'dummyServiceId'
real_vpc_endpoint_service_id = os.environ['VPC_SERVICE_ENDPOINT_ID']


def test_unsupported_action():
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId'
        },
        'RequestType': 'dummyAction',
    }
    context = []
    os.environ['ServiceId'] = test_vpc_endpoint_service_id
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert response['body'] == 'Unsupported action: dummyAction'


def test_create_invalid_vpc_endpoint_service_id():
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId'
        },
        'RequestType': 'Create',
    }
    context = []
    os.environ['ServiceId'] = test_vpc_endpoint_service_id
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert 'InvalidVpcEndpointServiceId.Malformed' in response['body']
    assert 'Invalid Id: \'dummyServiceId\'' in response['body']


def test_create_not_existing_vpc_endpoint_service_id():
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId'
        },
        'RequestType': 'Create',
    }
    context = []
    os.environ['ServiceId'] = 'vpce-svcnotexisting-0515bbd3ac7432640'
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert 'InvalidVpcEndpointServiceId.Malformed' in response['body']
    assert 'Invalid Id: \'vpce-svcnotexisting-0515bbd3ac7432640\'' in response['body']


def describe_vpc_endpoint_service_permissions(service_id):
    client = boto3.client('ec2')
    response = client.describe_vpc_endpoint_service_permissions(
        DryRun=False,
        ServiceId=service_id
    )
    return response

def delete_all_principals(service_id, principals_to_remove):
    client = boto3.client('ec2')
    response = client.modify_vpc_endpoint_service_permissions(
        DryRun=False,
        ServiceId=service_id,
        RemoveAllowedPrincipals=principals_to_remove
    )
    return response


def cleanup():
    os.environ['ServiceId'] = real_vpc_endpoint_service_id
    delete_all_principals(os.environ['ServiceId'],
        ['arn:aws:iam::dummyAccountId1:root', 'arn:aws:iam::dummyAccountId2:root'])


def test_create_one_permission():
    cleanup()
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId1'
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(os.environ['ServiceId'])
    assert len(response['AllowedPrincipals']) == 1
    assert response['AllowedPrincipals'][0]['Principal'] == 'arn:aws:iam::dummyAccountId1:root'


def test_create_two_permissions():
    cleanup()

    # create 1st principal
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId1'
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    # create 2nd principal
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId2'
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    # assert there are 2 principals
    response = describe_vpc_endpoint_service_permissions(os.environ['ServiceId'])
    assert len(response['AllowedPrincipals']) == 2
    assert response['AllowedPrincipals'][0]['Principal'] == 'arn:aws:iam::dummyAccountId1:root'
    assert response['AllowedPrincipals'][1]['Principal'] == 'arn:aws:iam::dummyAccountId2:root'


def test_delete_one_principal_when_no_permission_created():
    cleanup()

    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId1'
        },
        'RequestType': 'Delete',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(os.environ['ServiceId'])
    assert len(response['AllowedPrincipals']) == 0


def test_delete_one_permission_after_one_permission_created():
    cleanup()

    # create 1st principal
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId1'
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    # delete that principal
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId1'
        },
        'RequestType': 'Delete',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(os.environ['ServiceId'])
    assert len(response['AllowedPrincipals']) == 0


def test_update_permission_when_permission_exists():
    cleanup()
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId1'
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    event = {
        'ResourceProperties': {
            'OldAccountId': 'dummyAccountId1',
            'AccountId': 'dummyAccountId2'
        },
        'RequestType': 'Update',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(os.environ['ServiceId'])
    assert len(response['AllowedPrincipals']) == 1
    assert response['AllowedPrincipals'][0]['Principal'] == 'arn:aws:iam::dummyAccountId2:root'


def test_update_permission_when_no_permission_exists():
    cleanup()
    event = {
        'ResourceProperties': {
            'OldAccountId': 'dummyAccountId1',
            'AccountId': 'dummyAccountId2'
        },
        'RequestType': 'Update',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(os.environ['ServiceId'])
    assert len(response['AllowedPrincipals']) == 1
    assert response['AllowedPrincipals'][0]['Principal'] == 'arn:aws:iam::dummyAccountId2:root'


def setup_module(module):
    '''Clean up before the tests'''
    cleanup()


def teardown_module(module):
    '''Clean up after the tests'''
    cleanup()
