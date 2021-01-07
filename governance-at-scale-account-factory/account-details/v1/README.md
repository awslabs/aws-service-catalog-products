# account-details
# Description
This product takes a provided 'AccountName' and returns the details about that account 

## Usage 
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryAccountDetailsOrgRoleArn 
*Type:* String  
*Description:* The IAM Role in the Organizations root account that is assumable from the account where this is provisoned 
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountDetailsCRIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used for the AWS Lambda function when backing the account details custom resource

## Resources
The list of resources this template creates:

### Function 
*Type:* AWS::Lambda::Function  
*Description:* An AWS Lambda function to back an AWS CloudFormation custom resource. This expects a ResourceProperty of AccountType and
will return an organizational_unit_id based on the dict organizational_unit_ids
### Role 
*Type:* AWS::IAM::Role  
*Description:* An IAM role used as the execution role for the **Function** AWS Lambda function

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountDetailsCRArn 
*Description:* The ARN of the AWS Lambda function

## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-details` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-details
      Distributor: CCOE
      Name: account-details
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-details
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Tags: []
      Versions:
        - Description: This product takes a provided 'AccountName' and returns 
            the details about that account
          Name: v1
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v1
              RepositoryName: account-details
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-details` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-details:
    depends_on:
      - account-details-org-bootstrap
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:puppet_account
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/account-details/GovernanceAtScaleAccountFactoryAccountDetailsCRArn
          stack_output: GovernanceAtScaleAccountFactoryAccountDetailsCRArn
    parameters:
      GovernanceAtScaleAccountFactoryAccountDetailsCRIAMRoleName:
        default: AccountDetailsCRIAMRoleName
      GovernanceAtScaleAccountFactoryAccountDetailsOrgRoleArn:
        ssm:
          name: /governance-at-scale-account-factory/account-details-org-bootstrap/GovernanceAtScaleAccountFactoryAccountDetailsOrgRoleArn
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
    portfolio: demo-central-it-team-portfolio
    product: account-details
    version: v1
```