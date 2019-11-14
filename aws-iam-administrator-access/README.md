# aws-iam-administrator-access
Creates a role with the AdministratorAccess policy and a trust policy for the given account
Creates a role with the AdministratorAccess policy and a trust policy for the given service

## Description
Create AdministratorAccess policy attached roles

## Install Instructions

```bash
aws codecommit create-repository --repository-name aws-iam-administrator-access-assumable-role-account
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/aws-iam-administrator-access-assumable-role-account
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-iam-administrator-access/assumable-role-account/v1 aws-iam-administrator-access-assumable-role-account --force

aws codecommit create-repository --repository-name aws-iam-administrator-access-assumable-role-service
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/aws-iam-administrator-access-assumable-role-service
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-iam-administrator-access/assumable-role-service/v1 aws-iam-administrator-access-assumable-role-service --force
```
