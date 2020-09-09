# account-details-org-bootstrap
# Description
IAM Role needed to use AWS Organizations to list AWS Accounts.
 


## Parameters
The list of parameters for this template:

### ServiceCatalogToolsAccountId 
Type: String  
Description: The account where you have installed the Service Catalog tools. 
### GovernanceAtScaleAccountFactoryIAMRolePath 
Type: String  
Description: The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountDetailsOrgIAMRoleName 
Type: String  
Description: The name to use for IAM role that will be used to list accounts for bootstrapping purposes 

## Resources
The list of resources this template creates:

### AccountCreationDetailsAssumableRole 
Type: AWS::IAM::Role 
Description: IAM Role needed so we can list accounts
 

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountDetailsOrgRoleArn 
Description: The ARN for your Assumable role in root account  
