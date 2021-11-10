# aws-service-catalog-account-creation
# Description
This product is used to create a commercial AWS Account and bootstrap it using `aws-service-catalog-puppet` so you can provision products into the account
 
## Usage
Before provisioning this product, the account-bootstrap-shared product and the account-creation-shared product must both be provisioned into the same account, These two products build some resources needed for this product to work. They also provision the SSM parameters with the correct ARNs so this works without copy and pasting. 

## Parameters
The list of parameters for this template:

### Email 
*Type:* String  
*Description:* The email address to use for the commerical account that is to be created
### AccountName 
*Type:* String  
*Description:* The name to use for the account that is to be created 
### OrganizationAccountAccessRole 
*Type:* String  
*Default:* OrganizationAccountAccessRole  
*Description:* The name of the role to be created in the account that allows Organizations access 
### IamUserAccessToBilling 
*Type:* String  
*Default:* ALLOW  
*Descriptipon:* If set to ALLOW, this enables IAM users to access account billing information if they have the required permissions. If set to DENY, only the root user of the new account can access account billing information
### AccountGroup 
*Type:* String  
*Description:* Which platform does the account belong to 
### AccountType 
*Type:* String  
*Description:* Which stage of the SDLC is the account going to be used for 
### GovernanceAtScaleAccountFactoryAccountCreationCRArn 
*Type:* String  
*Description:* The ARN for the AWS Lambda function that creates the account
### GovernanceAtScaleAccountFactoryMoveToOUArn 
*Type:* String  
*Description:* The ARN of the AWS Lambda function that moves the new commercial account to the correct organizational unit
### GovernanceAtScaleAccountFactoryAccountWaiterArn 
*Type:* String  
*Description:* The ARN of the AWS Lambda function that waits for CodeBuild and CloudFormation to become available in the new commercial account
### GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn 
*Type:* String  
*Description:* The ARN of the AWS Lambda function that will bootstrap the new commerical account as a spoke of the current Service Catalog Puppet account
### GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn 
*Type:* String  
*Description:* The ARN of the AWS Lambda function that converts the account group and account type to the correct organizational unit
### GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn 
*Type:* String  
*Description:* The ARN of the AWS Lambda function that will dispatch SNS notifications on account creation
### ServiceCatalogPuppetVersion
*Type:* String  
*Description:* The version of Service Catalog Puppet in use

## Resources
The list of resources this template creates:

### OUDetails 
*Type:* Custom::Resource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn** AWS Lambda function to convert the account type and group into the correct organizational unit (OU)
### Account 
*Type:* Custom::CustomResource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountCreationCRArn** AWS Lambda function to create the new commercial account
### MoveToOU 
*Type:* Custom::CustomResource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryMoveToOUArn** AWS Lambda function to move the new account to the correct OU
### AccountWaiter1 
*Type:* Custom::CustomResource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountWaiterArn** AWS Lambda function to wait for CodeBuild and CloudFormation to become available in the new account
### Notifier 
*Type:* Custom::Resource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn** AWS Lambda function to send a notification when the new account is created
### Bootstrap 
*Type:* Custom::CustomResource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn** AWS Lambda function to bootstrap the new account

## Outputs
The list of outputs this template exposes:

### AccountId 
*Description:* The ID of the new account
   
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `aws-service-catalog-account-creation` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: aws-service-catalog-account-creation
      Distributor: CCOE
      Name: aws-service-catalog-account-creation
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: aws-service-catalog-account-creation
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Versions:
        - Description: This product is used to create a commercial AWS Account and bootstrap 
            it using `aws-service-catalog-puppet` so you can provision products into the account
          Name: v3
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v3
              RepositoryName: aws-service-catalog-account-creation
      ProviderName: ccoe
      Tags:
        - Key: team
          Value: ccoe
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `aws-service-catalog-account-creation` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file. This product is most commonly provisioned through Service Catalog Products UI in the AWS Console.
```yaml
launches:
  aws-service-catalog-account-factory-account:
    depends_on:
      - account-type-to-organizational-unit-chooser
      - account-details
      - account-create-update-notifier
      - account-bootstrap-shared
      - account-waiter
      - move-to-ou
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:puppet_account
    parameters:
      Email:
        default: emailme@example.com
      AccountGroup:
        default: workloads
      AccountName:
        default: devaccountforteamx
      AccountType:
        default: dev
      OrganizationAccountAccessRole:
        default: OrganizationAccountAccessRole
      IamUserAccessToBilling:
        default: ALLOW
      GovernanceAtScaleAccountFactoryAccountCreationCRArn:
        ssm:
          name: /governance-at-scale-account-factory/account-creation-shared/GovernanceAtScaleAccountFactoryAccountCreationCRArn
      GovernanceAtScaleAccountFactoryMoveToOUArn:
        ssm:
          name: /governance-at-scale-account-factory/move-to-ou/GovernanceAtScaleAccountFactoryMoveToOUCRArn
      GovernanceAtScaleAccountFactoryAccountWaiterArn:
        ssm:
          name: /governance-at-scale-account-factory/account-waiter/GovernanceAtScaleAccountFactoryAccountWaiterCRArn
      GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn:
        ssm:
          name: /governance-at-scale-account-factory/account-bootstrap-shared/GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn
      GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn:
        ssm:
          name: /governance-at-scale-account-factory/account-type-to-organizational-unit-chooser/GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn
      GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn:
        ssm:
          name: /governance-at-scale-account-factory/account-create-update-notifier/GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn
      ServiceCatalogPuppetVersion:
        default: 0.91.0
    portfolio: demo-central-it-team-portfolio
    product: aws-service-catalog-account-creation
    version: v3
```