# account-bootstrap-shared-org-bootstrap
# Description
IAM Role needed to use AWS Organizations to bootstrap AWS Accounts.
 


## Parameters
The list of parameters for this template:

### ServiceCatalogToolsAccountId 
Type: String  
Description: The account id you will be installing AWS Service Catalog Factory into 
### OrganizationAccountAccessRole 
Type: String 
Default: OrganizationAccountAccessRole 
Description: Name of the IAM role used to access cross accounts for AWS Orgs usage 
### GovernanceAtScaleAccountFactoryIAMRolePath 
Type: String  
Description: The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountBootstrapSharedBootstrapperOrgIAMRoleName 
Type: String  
Description: The name to use for IAM role that will be used to list accounts for bootstrapping purposes 

## Resources
The list of resources this template creates:

### AssumableRoleInRootAccount 
Type: AWS::IAM::Role 
Description: IAM Role needed by the account vending machine so it can bootstrap accounts
 

## Outputs
The list of outputs this template exposes:

### AssumableRoleArnInRootAccountForBootstrapping 
Description: The ARN for your Assumable role in root account  
