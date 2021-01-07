# account-details-org-bootstrap
# Description
This product creates an IAM Role that is needed to use AWS Organizations to list AWS Accounts.

## Usage 
This product should be provisioned in your Organization management account

## Parameters
The list of parameters for this template:

### ServiceCatalogToolsAccountId 
*Type:* String  
*Description:* The account ID fo the account where you have installed the Service Catalog Tools
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountDetailsOrgIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used to list accounts for bootstrapping purposes 

## Resources
The list of resources this template creates:

### AccountCreationDetailsAssumableRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM Role that can be assumed and allows for listing accounts in the organization
 

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountDetailsOrgRoleArn 
*Description:* The ARN for your assumable role in the organization root account  

## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-details-org-bootstrap` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-details-org-bootstrap
      Distributor: CCOE
      Name: account-details-org-bootstrap
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-details-org-bootstrap
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Tags: []
      Versions:
        - Description: This product creates an IAM Role that is needed to use 
            AWS Organizations to list AWS Accounts.
          Name: v1
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v1
              RepositoryName: account-details-org-bootstrap
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-details-org-bootstrap` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-details-org-bootstrap:
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:org_management
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/account-details-org-bootstrap/GovernanceAtScaleAccountFactoryAccountDetailsOrgRoleArn
          stack_output: GovernanceAtScaleAccountFactoryAccountDetailsOrgRoleArn
    parameters:
      GovernanceAtScaleAccountFactoryAccountDetailsOrgIAMRoleName:
        default: AccountDetailsOrgIAMRoleName
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
      ServiceCatalogToolsAccountId:
        default: SET_ME
    portfolio: demo-central-it-team-portfolio
    product: account-details-org-bootstrap
    version: v1
```