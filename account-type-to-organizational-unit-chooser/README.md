# account-type-to-organizational-unit-chooser
Takes the given account type and returns the organizational unit it should be assigned to

## Description
Deploys a lambda you can use to convert account type names to ou ids.  Currently this is hard coded ids in the lambda.

## Install Instructions

```bash
aws codecommit create-repository --repository-name account-type-to-organizational-unit-chooser
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-type-to-organizational-unit-chooser
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/account-type-to-organizational-unit-chooser/account-type-to-organizational-unit-chooser/v1 account-type-to-organizational-unit-chooser --force
```

