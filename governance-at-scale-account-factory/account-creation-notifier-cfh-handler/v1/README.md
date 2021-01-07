# account-creation-notifier-cfh-handler
# Description
This product creates an AWS Lambda as a subscription to an SNS topic. The Lambda function is used to relay messages from SNS to a custom HTTP POST endpoint
 
# Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### AccountCreateUpdateNotifierTopicArn 
*Type:* String   
*Description:* The ARN of the SNS topic to create the subscription for
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateCFHHandlerIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used for the AWS Lambda function

## Resources
The list of resources this template creates:

### Subscription
*Type:* AWS::SNS::Subscription  
*Description:* A subscription to the provided SNS topic that will trigger the **Function** AWS Lambda Function
### Permission
*Type:* AWS::Lambda::Permission  
*Desciption:* The permission that allows the provided SNS topic to invoke the **Function** AWS Lambda function
### Function 
*Type:* AWS::Lambda::Function  
*Description:* An AWS Lambda function the relays messages from the provided SNS topic to the provided HTTP POST endpoint 
### Role 
*Type:* AWS::IAM::Role  
*Description:* An IAM role used as the execution role for the **Function** AWS Lambda function
 
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-creation-notifier-cfh-handler` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-creation-notifier-cfh-handler
      Distributor: CCOE
      Name: account-creation-notifier-cfh-handler
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-creation-notifier-cfh-handler
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Tags: []
      Versions:
        - Description: This product creates an AWS Lambda as a subscription to an SNS topic. 
            The Lambda function is used to relay messages from SNS to a custom HTTP POST endpoint
          Name: v1
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v1
              RepositoryName: account-creation-notifier-cfh-handler
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-creation-notifier-cfh-handler` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-creation-notifier-cfh-handler:
    depends_on:
      - account-create-update-notifier
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:puppet_account
    parameters:
      AccountCreateUpdateNotifierTopicArn:
        ssm:
          name: /governance-at-scale-account-factory/account-create-update-notifier/AccountCreateUpdateNotifierTopicArn
      GovernanceAtScaleAccountFactoryAccountCreateUpdateCFHHandlerIAMRoleName:
        default: AccountCreateUpdateCFHHandlerIAMRoleName
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
      CFHAccountCreateUpdatePostUrl:
        default: https://example.com/intranet/teams/ccoe/products/account-factory/endpoint
    portfolio: demo-central-it-team-portfolio
    product: account-creation-notifier-cfh-handler
    version: v1
```