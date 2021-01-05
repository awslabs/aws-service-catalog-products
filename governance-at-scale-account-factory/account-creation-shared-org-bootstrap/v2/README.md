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
