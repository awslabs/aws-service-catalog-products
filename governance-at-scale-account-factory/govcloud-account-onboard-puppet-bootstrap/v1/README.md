# govcloud-account-onboard-puppet-bootstrap
# Description
The IAM role that **govcloud-account-onboard** requires in order to bootstrap a new GovCloud account as a spoke of the GovCloud Service Catalog Puppet account
 
## Usage
This product is intended to be used as part of the GovCloud account creation process. It must be provisioned in the GovCloud Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### OrganizationRootAccountId 
*Type:* String  
*Description:* The account ID of the Organization root in GovCloud
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
*Description:* IAM Role needed by GovCloud account onboarding to bootstrap Puppet
 

## Outputs
The list of outputs this template exposes:

### AssumableRoleArnInPuppetAccountForBootstrapping 
*Description:* The ARN for your assumable role in the Puppet account
