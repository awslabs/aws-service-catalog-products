# multi-account-cloudtrail-enable

This will enable AWS CloudTrail in all accounts for which it is deployed to.

## Description
You can choose which encryption to use for the buckets you create and you can choose whether to target
all regions or not.

## Install Instructions
```bash
aws codecommit create-repository --repository-name aws-cloudtrail-enable
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/aws-cloudtrail-enable
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/mulit-account-aws-cloudtrail/aws-cloudtrail-enable/v1 aws-cloudtrail-enable --force
```