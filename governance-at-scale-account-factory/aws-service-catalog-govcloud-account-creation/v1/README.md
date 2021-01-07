# aws-service-catalog-govcloud-account-creation
# Description
This product is used to create a new GovCloud account and the linked commercial AWS Accounts. The accounts will be moved to the organizational unit (OU) based on the provided account groups and account types. The new accounts will be bootstrapped with the Service Catalog Puppet account in the corresponding partition.
 
## Usage
There are a few requirements that must be met to successfully provision this product to create new GovCloud accounts:
1. This product must be provisioned in the Commercial Organization management account
2. You must already have a GovCloud Organization management account that is linked to the Commercial Organization management account
3. The `account-bootstrap-shared` product and the `account-creation-shared` product must both be provisioned in the Commercial Organization management account. These two products build some resources needed for this product to work. 
4. The `account-bootstrap-shared-org-bootstrap` and `govcloud-account-onboard` products must be provisioned in the GovCloud Organization management account. These are required for part of the process that automates the account invitation and acceptance as well as bootstrapping the new GovCloud member account 
5. The `account-bootstrap-shared` and `govcloud-account-onboard-puppet-bootstrap` products must be provisioned in the GovCloud Service Catalog Puppet account. These are required for part of the process that automates the account invitation and acceptance as well as bootstrapping the new GovCloud member account 
6. A `account-creation-notifier-cfh-handler` product must be provisioned in the Commercial Organization management account with the `CFHAccountCreateUpdatePostUrl` parameter set to the HTTP POST endpoint in the API Gateway that is created in the GovCloud Organization management account when the `govcloud-account-onboard` is provisioned. This value will look something like this: `https://{APIGWID}.execute-api.us-gov-west-1.amazonaws.com/Prod/onboard-account`. You will then use the ARN of this provisioned Lambda as the **GovernanceAtScaleAccountFactoryGovCloudAccountCreateUpdateNotifierCRArn** parameter value

## How it Works
An explanation of the steps that occur during this process can be found [here](how-it-works.md)

## Parameters
The list of parameters for this template:

### Email 
*Type:* String  
*Description:* The email address to use for the GovCloud and Commerical accounts that are to be created
### AccountName 
*Type:* String  
*Description:* The name to use for the accounts that are to be created 
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
*Description:* Which platform does the Commercial account belong to 
### AccountType 
*Type:* String  
*Description:* Which stage of the SDLC is the Commercial account going to be used for 
### GovCloudAccountGroup 
*Type:* String  
*Description:* Which platform does the GovCloud account belong to 
### GovCloudAccountType 
*Type:* String  
*Description:* Which stage of the SDLC is the GovCloud account going to be used for 
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
*Description:* The ARN of the AWS Lambda function that will dispatch SNS notifications on account creation of the Commercial account
### GovernanceAtScaleAccountFactoryGovCloudAccountCreateUpdateNotifierCRArn 
*Type:* String  
*Description:* The ARN of the AWS Lambda function that will dispatch SNS notifications on account creation of the GovCloud account
### ServiceCatalogPuppetVersion
*Type:* String  
*Description:* The version of Service Catalog Puppet in use
### PuppetAccountId
*Type:* String  
*Description:* The account ID for the Commercial account where Service Catalog Puppet is installed
### GovCloudPuppetAccountId
*Type:* String  
*Description:* The account ID for the GovCloud account where Service Catalog Puppet is installed

## Resources
The list of resources this template creates:

### OUDetails 
*Type:* Custom::Resource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn** AWS Lambda function to convert the account type and group into the correct organizational unit (OU) for the Commercial account
### GovCloudOUDetails 
*Type:* Custom::Resource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn** AWS Lambda function to convert the account type and group into the correct organizational unit (OU) for the GovCloud account
### Account 
*Type:* Custom::CustomResource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountCreationCRArn** AWS Lambda function to create the new Commercial and GovCloud accounts
### MoveToOU 
*Type:* Custom::CustomResource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryMoveToOUArn** AWS Lambda function to move the new Commercial account to the correct OU
### AccountWaiter1 
*Type:* Custom::CustomResource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountWaiterArn** AWS Lambda function to wait for CodeBuild and CloudFormation to become available in the new Commercial account
### Notifier 
*Type:* Custom::Resource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn** AWS Lambda function to send a notification when the new Commercial account is created
### GovCloudNotifier 
*Type:* Custom::Resource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryGovCloudAccountCreateUpdateNotifierCRArn** AWS Lambda function to send a notification when the new GovCloud account is created. This notification will make an HTTP POST to the API Gateway in the GovCloud Organization management account which executes an AWS Lambda function that completes the account onboarding process (invite to organization, accept invitation, move to correct OU and bootstrap) for the GovCloud account.
### Bootstrap 
*Type:* Custom::CustomResource  
*Description:* A custom resource using the **GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn** AWS Lambda function to bootstrap the new Commercial account

## Outputs
The list of outputs this template exposes:

### AccountId 
*Description:* The Account ID for the new Commercial account
### GovCloudAccountId 
*Description:* The Account ID for the new GovCloud account
  
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `aws-service-catalog-govcloud-account-creation` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: aws-service-catalog-govcloud-account-creation
      Distributor: CCOE
      Name: aws-service-catalog-govcloud-account-creation
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: aws-service-catalog-govcloud-account-creation
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Versions:
        - Description: This product is used to create a new GovCloud account and the linked commercial AWS Accounts. 
            The accounts will be moved to the organizational unit (OU) based on the provided account groups 
            and account types. The new accounts will be bootstrapped with the Service Catalog Puppet 
            account in the corresponding partition.
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v1
              RepositoryName: aws-service-catalog-govcloud-account-creation
      ProviderName: ccoe
      Tags:
        - Key: team
          Value: ccoe
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `aws-service-catalog-govcloud-account-creation` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file. This product is most commonly provisioned through Service Catalog Products UI in the AWS Console.
```yaml
launches:
  aws-service-catalog-govcloud-account-factory-account:
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
      AccountName:
        default: devaccountforteamx
      AccountGroup:
        default: workloads
      AccountType:
        default: dev
      GovCloudAccountGroup:
        default: workloads
      GovCloudAccountType:
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
      GovernanceAtScaleAccountFactoryGovCloudAccountCreateUpdateNotifierCRArn:
        ssm:
          name: /governance-at-scale-account-factory/account-create-update-notifier/GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn
      ServiceCatalogPuppetVersion:
        default: 0.91.0
      PuppetAccountId:
        default: SET_ME
      GovCloudPuppetAccountId:
        default: SET_ME
    portfolio: demo-central-it-team-portfolio
    product: aws-service-catalog-account-creation
    version: v3
```