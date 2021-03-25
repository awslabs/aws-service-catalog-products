# account-puppet-org-bootstrap
# Description
This product creates the IAM role that is required in order to bootstrap a new account as a spoke of the Puppet account
 
## Usage
This product is intended to be used as part of both the GovCloud and Commercial account creation process. It must be provisioned in the corresponding Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### OrganizationRootAccountId 
*Type:* String  
*Description:* The account ID of the Organization root 
### OrganizationAccountAccessRole 
*Type:* String  
*Default:* OrganizationAccountAccessRole  
*Description:* Name of the IAM role used to access cross accounts for AWS Organizations usage 
### AccountOnboardPuppetRoleName 
*Type:* String  
*Description:* The name to use for IAM role that will be used to bootstrap an account 

## Resources
The list of resources this template creates:

### AssumableRoleInPuppetAccount 
*Type:* AWS::IAM::Role  
*Description:* An assumable IAM Role that allows the govcloud-account-onboard and account-bootstrap-shared products to bootstrap accounts with Service Catalog Puppet
 

## Outputs
The list of outputs this template exposes:

### AssumableRoleArnInPuppetAccountForBootstrapping 
*Description:* The ARN for your assumable role in the Puppet account

## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-puppet-org-bootstrap` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-puppet-org-bootstrap
      Distributor: CCOE
      Name: account-puppet-org-bootstrap
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-puppet-org-bootstrap
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Versions:
        - Description: This product creates the IAM role that govcloud-account-onboard and 
            account-bootstrap-shared require in order to bootstrap a new account as a 
            spoke of the Service Catalog Puppet account
          Name: v1
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v1
              RepositoryName: account-puppet-org-bootstrap
      ProviderName: ccoe
      Tags:
        - Key: team
          Value: ccoe
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-puppet-org-bootstrap` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file.
```yaml
launches:
  account-puppet-org-bootstrap:
    parameters:
      OrganizationRootAccountId:
        default: SET_ME
      OrganizationAccountAccessRole:
        default: OrganizationAccountAccessRole
      AccountOnboardPuppetRoleName:
        default: PuppetAccountAccessRole
    portfolio: demo-central-it-team-portfolio
    product: account-puppet-org-bootstrap
    version: v1
    deploy_to:
      tags:
        - tag: scope:puppet_account
          regions: default_region  
```