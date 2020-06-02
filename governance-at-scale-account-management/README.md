# governance-at-scale-account-management

## Description
This product set will listen to the account creation process in the product set 
aws-control-tower-augmented-account-factory and will record the results in its datastore for consumption by Cloud 
Financial Hub 

## Install Instructions

```bash
aws codecommit create-repository --repository-name datastore
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/datastore
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-augmented-account-factory/datastore/v1 datastore --force

aws codecommit create-repository --repository-name account-recorder
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-recorder
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-control-tower-augmented-account-factory/account-recorder/v1 account-recorder --force
```