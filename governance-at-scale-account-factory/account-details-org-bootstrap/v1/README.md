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
