import os
import json
import boto3
from spoke_lambda import (
    lambda_handler, decode_log_result)


real_vpc_endpoint_role = os.environ['VPC_ENDPOINT_ROLE']
real_lambda_name = os.environ['HUB_LAMBDA_FUNCTION_NAME']

def test_when_user_not_authorized():
    os.environ['VPCE_PERM_ROLE_ARN'] = 'dummy-must-have-min-20-characters'
    os.environ['FUNC_NAME'] = 'dummy'
    event = {}
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert 'AccessDenied' in response['body']
    assert 'not authorized to perform: sts:AssumeRole' in response['body']


def test_hub_lambda_not_found():
    os.environ['VPCE_PERM_ROLE_ARN'] = real_vpc_endpoint_role
    os.environ['FUNC_NAME'] = 'dummy'
    event = {}
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert 'Function not found' in response['body']


def test_lambda_log_result_decode():
    log_result = 'U1RBUlQgUmVxdWVzdElkOiBkYTc2ZGU2ZC1jNDNjLTQ5NGUtYmEyYi0yZGQ3YzVjZDhlMTggVmVyc2lvbjogJExBVEVTVApbSU5GT10JMjAyMS0xMi0xMFQyMzoyNToxNi45OTdaCWRhNzZkZTZkLWM0M2MtNDk0ZS1iYTJiLTJkZDdjNWNkOGUxOAl7fQpbRVJST1JdIEtleUVycm9yOiAnUmVzb3VyY2VQcm9wZXJ0aWVzJwpUcmFjZWJhY2sgKG1vc3QgcmVjZW50IGNhbGwgbGFzdCk6CsKgwqBGaWxlICIvdmFyL3Rhc2svYXBwLnB5IiwgbGluZSAxMDksIGluIGxhbWJkYV9oYW5kbGVyCsKgwqDCoMKgYWNjb3VudF9pZCA9IGV2ZW50WydSZXNvdXJjZVByb3BlcnRpZXMnXVsnQWNjb3VudElkJ11FTkQgUmVxdWVzdElkOiBkYTc2ZGU2ZC1jNDNjLTQ5NGUtYmEyYi0yZGQ3YzVjZDhlMTgKUkVQT1JUIFJlcXVlc3RJZDogZGE3NmRlNmQtYzQzYy00OTRlLWJhMmItMmRkN2M1Y2Q4ZTE4CUR1cmF0aW9uOiAxLjQyIG1zCUJpbGxlZCBEdXJhdGlvbjogMiBtcwlNZW1vcnkgU2l6ZTogMTI4IE1CCU1heCBNZW1vcnkgVXNlZDogNjMgTUIJCg=='
    decoded = decode_log_result(log_result)
    assert "[ERROR] KeyError: 'ResourceProperties'" in decoded


def test_hub_lambda_account_id_not_set():
    os.environ['VPCE_PERM_ROLE_ARN'] = real_vpc_endpoint_role
    os.environ['FUNC_NAME'] = real_lambda_name
    event = {}
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert response['responseStatus'] == 'FAILED'
    assert "KeyError: 'ResourceProperties'" in response['body']


def test_hub_lambda_create():
    os.environ['VPCE_PERM_ROLE_ARN'] = real_vpc_endpoint_role
    os.environ['FUNC_NAME'] = real_lambda_name
    event = {
        'ResourceProperties': {
            'AccountId': 'dummyAccountId1',
            'Action': 'create',
        }
    }
    context = []
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['responseStatus'] == 'SUCCESS'
