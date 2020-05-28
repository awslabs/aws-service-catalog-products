# aws-control-tower-augmented-account-factory
Wrapper for AWS Control Tower Account Factory.  Improves the customer user experience and dispatches the result

## Description
This product will use the AWS Control Tower Account Factory product to create an AWS account.  It will expose parameters
for the account that are more user friendly.  Once the creation has completed the account id will be available as a 
output to the product.  

## Install Instructions
You will need to provision an AWS CloudFormation stack for account-details-to-aws-account-id/v1/org-bootstrap.template.yaml
This will create an IAM Role needed as a parameter for the account-details-to-aws-account-id stack.

```bash
aws codecommit create-repository --repository-name account-type-to-organizational-unit-chooser
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-type-to-organizational-unit-chooser
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-augmented-account-factory/account-type-to-organizational-unit-chooser/v4 account-type-to-organizational-unit-chooser --force

aws codecommit create-repository --repository-name account-details-to-aws-account-id
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-details-to-aws-account-id
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-augmented-account-factory/account-details-to-aws-account-id/v1 account-details-to-aws-account-id --force

aws codecommit create-repository --repository-name augmented-account-factory
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/augmented-account-factory
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-augmented-account-factory/augmented-account-factory/v4 augmented-account-factory --force

aws codecommit create-repository --repository-name account-creation-notifier
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-creation-notifier
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-account-creation-notifier/account-creation-notifier/v1 account-creation-notifier --force

aws codecommit create-repository --repository-name account-bootstrap-shared
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-bootstrap-shared
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-account-creation-notifier/account-bootstrap-shared/v3 account-bootstrap-shared --force
```