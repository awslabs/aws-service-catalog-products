# vpc-endpoint-permissions-role

This Service Catalog Product creates an IAM Role. It is supposed to be deployed in the Networking Master AWS Account.

## Tests

### Validate AWS CloudFormation templates

You can run the following command locally to validate the AWS CloudFormation template:
```
aws cloudformation validate-template --template-body file://v1/product.template.yaml
```

### Run manual integrations tests

Ensure there is already a VPC Endpoint Service created in the Networking Master AWS Account and that you know its ID.

Deploy the CFN template manually **in the Networking Master AWS Account**:
```
aws cloudformation deploy --template-file v1/product.template.yaml --stack-name sct-product-vpc-endpoint-permissions-role-manual --capabilities CAPABILITY_NAMED_IAM --parameter-overrides pPuppetHubAccountId=TODO pVpcEndpointPermissionsServiceId=TODO
```

Verify that this command works:
```
aws ec2 describe-vpc-endpoint-service-permissions --service-id TODO
```

Delete the CFN stack:
```
aws cloudformation delete-
stack --stack-name sct-product-vpc-endpoint-permissions-role-manual
```
