# account-vending
This is a solution to help deliver an account vending machine.

## Description
This creates an AWS Account vending machine so your customers can create their own AWS Accounts using AWS Service Catalog.

There are three AWS Service Catalog Products in this solution.
  
```account-bootstrap-shared``` and ```account-creation-shared``` will provision lambdas into an account that can assume 
an IAM Role that has AWS Organizations access to create accounts.  These products export AWS Lambda function ARNs that
can be used with the account-creation product to create accounts.

```account-creation``` will use the exported ARNs from ```account-bootstrap-shared``` and ```account-creation-shared```
to create an AWS account. 

## Install instructions
1. ```org-bootstrap.template.yaml``` should be provisioned into your AWS Organizations root account.  This will create 
an IAM role.  This template has a parameter named ```ServiceCatalogFactoryAccountId``` which is the account id of your 
aws-service-catalog-factory account.  The template exports the ARN for the role so you can use it later.
1. Copy the configuration from portfolio.yaml into your portfolio.
1. Create the AWS Code Commit repos, clone them and then add the code:
```bash
aws codecommit create-repository --repository-name account-vending-account-creation-shared
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-vending-account-creation-shared
svn export https://github.com/eamonnfaherty/cloudformation-templates/trunk/account-vending/account-creation-shared/v1 account-vending-account-creation-shared --force

aws codecommit create-repository --repository-name account-vending-account-bootstrap-shared
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-vending-account-bootstrap-shared
svn export https://github.com/eamonnfaherty/cloudformation-templates/trunk/account-vending/account-bootstrap-shared/v1 account-vending-account-bootstrap-shared --force

aws codecommit create-repository --repository-name account-vending-account-creation
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/account-vending-account-creation
svn export https://github.com/eamonnfaherty/cloudformation-templates/trunk/account-vending/account-creation/v1 account-vending-account-creation --force
```

## Usage instructions
Copy the config from ```manifest.yaml```.  ```account-vending-account-creation-shared``` and 
```account-vending-account-bootstrap-shared``` should appear in your manifest only once.  You should add a modified 
version of ```account-vending-account-001``` for every account you want to create using aws-service-catalog-puppet.