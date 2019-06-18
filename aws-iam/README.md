# aws-iam
This is a solution to help deliver useful IAM roles

## Description
Deploys a highly configurable IAM Group/Role strategy that allows users to assume roles into other accounts from the security account. Using IAM Groups ensures permissions are for users in those assumed roles are locked down.

## Install Instructions

```bash
aws codecommit create-repository --repository-name iam-assume-roles-spoke
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/iam-assume-roles-spoke
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-iam/iam-assume-roles-spoke/v1 iam-assume-roles-spoke --force

aws codecommit create-repository --repository-name iam-groups-security-account
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/iam-groups-security-account
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-iam/iam-groups-security-account/v1 iam-groups-security-account --force
```

