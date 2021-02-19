# account-create-update-notifier
# Description
This product creates an AWS Lambda function to back a custom resource that dispatches notifications to an included SNS Topic
 
## Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateCRIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used for the AWS Lambda that backs a custom resource 

## Resources
The list of resources this template creates:

### SNSTopic 
*Type:* AWS::SNS::Topic  
*Description:* An SNS Topic others can subscribe to so that they can find out about account creations 
### Function 
*Type:* AWS::Lambda::Function  
*Description:* An AWS Lambda function to dispatch notifications to the SNSTopic 
### Role 
*Type:* AWS::IAM::Role  
*Description:* The IAM role that is needed to publish account creations to SNS
 

## Outputs
The list of outputs this template exposes:

### AccountCreateUpdateNotifierTopicArn 
*Description:* The ARN of the SNS topic  
### AccountCreateUpdateNotifierTopicName 
*Description:* The name of the SNS topic
### GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn 
*Description:* The ARN of the AWS Lambda function that can be used to back custom resources to notify others that accounts have been created
   
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-create-update-notifier` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-create-update-notifier
      Distributor: CCOE
      Name: account-create-update-notifier
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-create-update-notifier
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Tags: []
      Versions:
        - Description: This product creates an AWS Lambda function to back a custom resource 
            that dispatches notifications to an included SNS Topic
          Name: v2
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v2
              RepositoryName: account-create-update-notifier
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-create-update-notifier` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-create-update-notifier:
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:puppet_account
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/account-create-update-notifier/AccountCreateUpdateNotifierTopicArn
          stack_output: AccountCreateUpdateNotifierTopicArn
        - param_name: /governance-at-scale-account-factory/account-create-update-notifier/AccountCreateUpdateNotifierTopicName
          stack_output: AccountCreateUpdateNotifierTopicName
        - param_name: /governance-at-scale-account-factory/account-create-update-notifier/GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn
          stack_output: GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn
    parameters:
      GovernanceAtScaleAccountFactoryAccountCreateUpdateCRIAMRoleName:
        default: AccountCreateUpdateCRIAMRoleName
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
    portfolio: demo-central-it-team-portfolio
    product: account-create-update-notifier
    version: v2
```