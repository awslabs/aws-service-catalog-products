# account-type-to-organizational-unit-chooser
# Description
This product takes the given account type and returns the organizational unit it should be assigned to
 
## Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountTypeChooserCRIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used to list accounts for bootstrapping purposes 

## Resources
The list of resources this template creates:

### Function 
*Type:* AWS::Lambda::Function  
*Description:* An AWS Lambda function to back an AWS CloudFormation custom resource. This expects a ResourceProperty of AccountType and
will return an organizational_unit_id based on the dict organizational_unit_ids
 
### Role 
*Type:* AWS::IAM::Role  
*Description:* An IAM role that serves as the execution role for the AWS Lambda function
 

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn 
*Description:* The ARN of the AWS Lambda function
  
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-type-to-organizational-unit-chooser` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-type-to-organizational-unit-chooser
      Distributor: CCOE
      Name: account-type-to-organizational-unit-chooser
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-type-to-organizational-unit-chooser
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Tags: []
      Versions:
        - Description: This product takes the given account type and returns the 
            organizational unit it should be assigned to
          Name: v2
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v2
              RepositoryName: account-type-to-organizational-unit-chooser
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-type-to-organizational-unit-chooser` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-type-to-organizational-unit-chooser:
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:puppet_account
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/account-type-to-organizational-unit-chooser/GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn
          stack_output: GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn
    parameters:
      GovernanceAtScaleAccountFactoryAccountTypeChooserCRIAMRoleName:
        default: AccountTypeChooserCRIAMRoleName
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
    portfolio: demo-central-it-team-portfolio
    product: account-type-to-organizational-unit-chooser
    version: v2
```