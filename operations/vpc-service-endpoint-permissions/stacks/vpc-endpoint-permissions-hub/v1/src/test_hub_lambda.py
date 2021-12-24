import os
import json
import boto3
from hub_lambda import (
    lambda_handler)


test_vpc_endpoint_service_id = 'dummyServiceId'
real_vpc_endpoint_service_id = os.environ['VPC_SERVICE_ENDPOINT_ID']
networking_account_id = os.environ['NETWORKING_ACCOUNT_ID']
role_arn_in_networking_account = f'arn:aws:iam::{networking_account_id}:role/vpc-service-endpoint-permissions-networking'


def test_account_id_not_set():
    event = {
        'parameters': {
            # 'AccountId': 'dummyAccountId',
            'RoleARNInNetworkingAccountId': 'dummyRoleInNetworkingAccountId'
        },
    }
    context = []
    os.environ['ServiceId'] = test_vpc_endpoint_service_id
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert 'KeyError: \'AccountId\'' in response['body']
    assert 'AccountId' in response['body']


def test_action_not_set():
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId',
            'RoleARNInNetworkingAccountId': 'dummyRoleInNetworkingAccountId'
        },
        #'RequestType': 'dummyAction',
    }
    context = []
    os.environ['ServiceId'] = test_vpc_endpoint_service_id
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert 'KeyError: \'RequestType\'' in response['body']


def test_role_innetworking_account_id_not_set():
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId',
            # 'RoleARNInNetworkingAccountId': 'dummyRoleInNetworkingAccountId'
        },
        'RequestType': 'dummyAction',
    }
    context = []
    os.environ['ServiceId'] = test_vpc_endpoint_service_id
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert 'KeyError: \'RoleARNInNetworkingAccountId\'' in response['body']


def get_current_account_id():
    client = boto3.client('sts')
    account_id = client.get_caller_identity()["Account"]
    return account_id


def test_unsupported_action():
    account_id = get_current_account_id()
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId',
            'RoleARNInNetworkingAccountId': 'dummyRoleInNetworkingAccountId'
        },
        'RequestType': 'dummyAction',
    }
    context = []
    os.environ['ServiceId'] = test_vpc_endpoint_service_id
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert 'Unsupported action: dummyAction' in response['body']


def test_create_invalid_vpc_endpoint_service_id():
    account_id = get_current_account_id()
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId',
            'RoleARNInNetworkingAccountId': 'dummyRoleInNetworkingAccountId'
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
    account_id = get_current_account_id()
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId',
            'RoleARNInNetworkingAccountId': 'dummyRoleInNetworkingAccountId'
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


def describe_vpc_endpoint_service_permissions(boto3_session, service_id):
    client = boto3_session.client('ec2')
    response = client.describe_vpc_endpoint_service_permissions(
        DryRun=False,
        ServiceId=service_id
    )
    return response


def delete_all_principals(boto3_session, service_id, principals_to_remove):
    client = boto3_session.client('ec2')
    response = client.modify_vpc_endpoint_service_permissions(
        DryRun=False,
        ServiceId=service_id,
        RemoveAllowedPrincipals=principals_to_remove
    )
    return response


def assume_role():
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


def cleanup(boto3_session, service_id):
    delete_all_principals(boto3_session, service_id,
        ['arn:aws:iam::dummyAccountId1:root', 'arn:aws:iam::dummyAccountId2:root'])


def test_create_one_permission():
    service_id = real_vpc_endpoint_service_id
    os.environ['ServiceId'] = service_id

    boto3_session = assume_role()
    cleanup(boto3_session, service_id)
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId1',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(boto3_session, service_id)
    assert len(response['AllowedPrincipals']) == 1
    assert response['AllowedPrincipals'][0]['Principal'] == 'arn:aws:iam::dummyAccountId1:root'


def test_create_two_permissions():
    service_id = real_vpc_endpoint_service_id
    os.environ['ServiceId'] = service_id

    boto3_session = assume_role()
    cleanup(boto3_session, service_id)

    # create 1st principal
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId1',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    # create 2nd principal
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId2',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    # assert there are 2 principals
    response = describe_vpc_endpoint_service_permissions(boto3_session, service_id)
    assert len(response['AllowedPrincipals']) == 2
    assert response['AllowedPrincipals'][0]['Principal'] == 'arn:aws:iam::dummyAccountId1:root'
    assert response['AllowedPrincipals'][1]['Principal'] == 'arn:aws:iam::dummyAccountId2:root'


def test_delete_one_principal_when_no_permission_created():
    service_id = real_vpc_endpoint_service_id
    os.environ['ServiceId'] = service_id

    boto3_session = assume_role()
    cleanup(boto3_session, service_id)

    event = {
        'parameters': {
            'AccountId': 'dummyAccountId1',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Delete',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(boto3_session, service_id)
    assert len(response['AllowedPrincipals']) == 0


def test_delete_one_permission_after_one_permission_created():
    service_id = real_vpc_endpoint_service_id
    os.environ['ServiceId'] = service_id

    boto3_session = assume_role()
    cleanup(boto3_session, service_id)

    # create 1st principal
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId1',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    # delete that principal
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId1',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Delete',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(boto3_session, service_id)
    assert len(response['AllowedPrincipals']) == 0


def test_update_permission_when_permission_exists():
    service_id = real_vpc_endpoint_service_id
    os.environ['ServiceId'] = service_id

    boto3_session = assume_role()
    cleanup(boto3_session, service_id)
    event = {
        'parameters': {
            'AccountId': 'dummyAccountId1',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Create',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    event = {
        'parameters': {
            'OldAccountId': 'dummyAccountId1',
            'AccountId': 'dummyAccountId2',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Update',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(boto3_session, service_id)
    assert len(response['AllowedPrincipals']) == 1
    assert response['AllowedPrincipals'][0]['Principal'] == 'arn:aws:iam::dummyAccountId2:root'


def test_update_permission_when_no_permission_exists():
    service_id = real_vpc_endpoint_service_id
    os.environ['ServiceId'] = service_id

    boto3_session = assume_role()
    cleanup(boto3_session, service_id)
    event = {
        'parameters': {
            'OldAccountId': 'dummyAccountId1',
            'AccountId': 'dummyAccountId2',
            'RoleARNInNetworkingAccountId': role_arn_in_networking_account
        },
        'RequestType': 'Update',
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'

    response = describe_vpc_endpoint_service_permissions(boto3_session, service_id)
    assert len(response['AllowedPrincipals']) == 1
    assert response['AllowedPrincipals'][0]['Principal'] == 'arn:aws:iam::dummyAccountId2:root'


def setup_module(module):
    '''Clean up before the tests'''
    boto3_session = assume_role()
    cleanup(boto3_session, real_vpc_endpoint_service_id)


def teardown_module(module):
    '''Clean up after the tests'''
    boto3_session = assume_role()
    cleanup(boto3_session, real_vpc_endpoint_service_id)
