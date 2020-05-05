# aws-control-tower-augmented-account-factory
Wrapper for AWS Control Tower Account Factory.  Improves the customer user experience and dispatches the result

## Description


## Install Instructions

```bash
aws codecommit create-repository --repository-name account-type-to-organizational-unit-chooser
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-type-to-organizational-unit-chooser
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-augmented-account-factory/account-type-to-organizational-unit-chooser/v1 account-type-to-organizational-unit-chooser --force

aws codecommit create-repository --repository-name account-details-to-aws-account-id
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-details-to-aws-account-id
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-augmented-account-factory/account-details-to-aws-account-id/v1 account-details-to-aws-account-id --force

aws codecommit create-repository --repository-name augmented-account-factory
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/augmented-account-factory
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-augmented-account-factory/augmented-account-factory/v1 augmented-account-factory --force
```