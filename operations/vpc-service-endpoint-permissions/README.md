# VPC Endpoint Permissions

This solution adds a spoke account id to utilise a VPC Endpoint in an AWS Multi-Account environment. This is typically used when sharing Gateway Loadbalancers from a core networking account to spoke accounts.

Hub Account Resources:
![Template Design](operations/vpc-endpoint-permissions/stacks/vpc-endpoint-permissions-hub/v1/vpc-endpoint-permissions-hub.drawio)

Spoke Account Resources:
![Template Design](operations/vpc-endpoint-permissions/stacks/vpc-endpoint-permissions-spoke/v1/vpc-endpoint-permissions-spoke.drawio)

## Description

* This product is comprised of two sub-products- a Hub product that creates an IAM role and Lambda function
* The Lambda function in the Networking hub account is triggered as a custom resource from the calling spoke account, allowing the addition of permissions to the VPC Endpoint resource

## Validate AWS CloudFormation templates

You can run the following command to validate the AWS CloudFormation templates:
```
aws cloudformation validate-template --template-body file://product.template.yaml
```

## Run integrations tests

These tests interact with an AWS Account.

### Testing the Hub Lambda

You have to ensure that:
1. You have programmatic access to the Hub AWS Account
2. You have a VPC Endpoint Service deployed

Set up local environment:
```
cd operations/vpc-service-endpoint-permissions/stacks/vpc-endpoint-permissions-hub/
python3 -m venv ./venv
source venv/bin/activate
pip install -r v1/requirements_dev.txt
```

Run Pytest tests:
```
export VPC_SERVICE_ENDPOINT_ID=TODO
pytest --verbose v1/src/test_hub_lambda.py
```

### Testing the Spoke Lambda

You have to ensure that:
1. You have programmatic access to the Spoke AWS Account
2. In the Hub Account, you have created a Role, which can be assumed from the Spoke AWS Account, e.g. `arn:aws:iam::TODO:role/VPCEndpointModifier`
3. In the Hub Account, the Hub lambda function was deployed. You can zip the Hub lambda by:
```
cd operations/vpc-service-endpoint-permissions/stacks/vpc-endpoint-permissions-hub/
cp v1/src/hub_lambda.py venv/lib/python3.9/site-packages
cd venv/lib/python3.9/site-packages
rm -f hub_lambda.zip
zip -r hub_lambda.zip .
```
When deploying this Lambda function, please:
* set ServiceId environment variable
* set the lambda handler

Set up local environment:
```
cd operations/vpc-service-endpoint-permissions/stacks/vpc-endpoint-permissions-spoke/
python3 -m venv ./venv
source venv/bin/activate
pip install -r v1/requirements_dev.txt
```

Run Pytest tests:
```
export VPC_ENDPOINT_ROLE="arn:aws:iam::TODO:role/VPCEndpointModifier"
export HUB_LAMBDA_FUNCTION_NAME="vpc_endpoint_modifier"
pytest --verbose v1/src/test_spoke_lambda.py
```
