# vpc-endpoint-permissions-role

This Service Catalog Product creates an IAM Role. It is supposed to be deployed in the networking AWS Account.

## Manual tests

You can run the following command locally to validate the AWS CloudFormation template:
```
aws cloudformation validate-template --template-body file://v1/product.template.yaml
```

Deploy the CFN template manually **in the networking AWS Account**:
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
