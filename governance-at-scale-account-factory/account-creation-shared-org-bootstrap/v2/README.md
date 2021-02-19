# account-creation-shared-org-bootstrap
# Description
This product creates an IAM Role that is needed in order to use AWS Organizations to create AWS Accounts
 
## Usage
This product should be provisioned in your Organization management account

## Parameters
The list of parameters for this template:

### ServiceCatalogToolsAccountId 
*Type:* String  
*Description:* The account ID of the account where you have installed AWS Service Catalog Factory 
### OrganizationAccountAccessRole 
*Type:* String  
*Default:* OrganizationAccountAccessRole  
*Description:* The name of the IAM role used to access cross accounts for AWS Organizations usage 
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountCreationSharedOrgIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used to list accounts for bootstrapping purposes

## Resources
The list of resources this template creates:

### AssumableRoleInRootAccount 
*Type:* AWS::IAM::Role  
*Description:* An IAM Role to be used by the account vending machine so it can create and move accounts

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn 
*Description:* The ARN for the assumable role in the organization root account  
 
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-creation-shared-org-bootstrap` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-creation-shared-org-bootstrap
      Distributor: CCOE
      Name: account-creation-shared-org-bootstrap
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-creation-shared-org-bootstrap
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Tags: []  
      Versions:
        - Description: This product creates an IAM Role that is needed in order 
            to use AWS Organizations to create AWS Accounts
          Name: v2
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v2
              RepositoryName: account-creation-shared-org-bootstrap
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-creation-shared-org-bootstrap` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-creation-shared-org-bootstrap:
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:org_management
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/account-creation-shared-org-bootstrap/GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn
          stack_output: GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn
    parameters:
      GovernanceAtScaleAccountFactoryAccountCreationSharedOrgIAMRoleName:
        default: AccountCreationSharedOrgIAMRoleName
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
      OrganizationAccountAccessRole:
        default: OrganizationAccountAccessRole
      ServiceCatalogToolsAccountId:
        default: SET_ME
    portfolio: demo-central-it-team-portfolio
    product: account-creation-shared-org-bootstrap
    version: v2
```