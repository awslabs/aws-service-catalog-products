# SecurityHub
This is a solution that will set up AWS Security Hub in a Hub and Spoke style model.

## Description
AWS Security Hub provides you with a comprehensive view of your security state in AWS and helps you check your compliance with the security industry standards and best practices. Security Hub collects security data from across AWS accounts, services, and supported third-party partner products and helps you analyze your security trends and identify the highest priority security issues.

## Install Instructions

```bash
aws codecommit create-repository --repository-name securityhub-master
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/securityhub-master
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/multi-account-aws-securityhub/securityhub-master/v1 securityhub-master --force

aws codecommit create-repository --repository-name securityhub-spoke
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/securityhub-spoke
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/multi-account-aws-securityhub/securityhub-spoke/v1 securityhub-spoke --force
```
