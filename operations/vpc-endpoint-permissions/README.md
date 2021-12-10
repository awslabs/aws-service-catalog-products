# VPC Endpoint Permissions

This solution adds a spoke account id to utilise a VPC Endpoint in an AWS Multi-Account environment. This is typically used when sharing Gateway Loadbalancers from a core networking account to spoke accounts.

Hub Account Resources:
![Template Design](operations/vpc-endpoint-permissions/stacks/vpc-endpoint-permissions-hub/v1/vpc-endpoint-permissions-hub.drawio)

Spoke Account Resources:
![Template Design](operations/vpc-endpoint-permissions/stacks/vpc-endpoint-permissions-spoke/v1/vpc-endpoint-permissions-spoke.drawio)

## Description

* This product is comprised of two sub-products- a Hub product that creates an IAM role and Lambda function
* The Lambda function in the Networking hub account is triggered as a custom resource from the calling spoke account, allowing the addition of permissions to the VPC Endpoint resource

## Run integrations tests

These tests interact with an AWS Account.

### Testing the Hub Lambda

You have to ensure that:
1. You have programmatic access to the Hub AWS Account
2. You have a VPC Endpoint Service deployed

Set up local environment:
```
cd vpc-endpoint-permissions/stacks/vpc-endpoint-permissions-hub/
python3 -m venv ./venv
source venv/bin/activate
pip install -r v1/src/requirements_dev.txt
```

Run Pytest tests:
```
export VPC_SERVICE_ENDPOINT_ID=TODO
pytest --verbose v1/src/test_hub_lambda.py
```
