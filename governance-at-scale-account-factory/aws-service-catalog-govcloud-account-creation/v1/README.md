# aws-service-catalog-govcloud-account-creation
# Description
This must be provisioned in a management account of your organization in the commercial region. account-bootstrap-shared-product and account-creation-shared-product must both be provisioned into the same accountbefore this will work - they build some resources needed for this to work and they provision the SSM params with thecorrect ARNs so this works with no copy and pasting.Provisioning this template will create an AWS Account and bootstrap it using aws-service-catalog-puppet so you canprovision products into the account.
 


## Parameters
The list of parameters for this template:

### Email 
Type: String  
Description: The email address to use for the account that is to be created 
### AccountName 
Type: String  
Description: The name to use for the account that is to be created 
### OrganizationAccountAccessRole 
Type: String 
Default: OrganizationAccountAccessRole 
Description: The name of the role to be created in the account that allows Organizations access 
### IamUserAccessToBilling 
Type: String 
Default: ALLOW  
### AccountGroup 
Type: String  
Description: Which platform does the account belong to 
### AccountType 
Type: String  
Description: Which stage of the SDLC is the account going to be used for 
### GovernanceAtScaleAccountFactoryAccountCreationCRArn 
Type: String 
Default: account-vending-creation-lambda 
Description: The ARN of the account creation lambda 
### GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn 
Type: String 
Default: account-vending-bootstrapper-lambda 
Description: The ARN of the account bootstrapping lambda 
### GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn 
Type: String  
Description: The ARN of the lambda that converts group and type to Arn 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn 
Type: String  
Description: The ARN of the lambda that will dispatch SNS notifications on account creation / update 

## Resources
The list of resources this template creates:

### OUDetails 
Type: Custom::Resource  
### Account 
Type: Custom::CustomResource 
Description: A custom resource representing an AWS Account 
### Notifier 
Type: Custom::Resource  
### Bootstrap 
Type: Custom::CustomResource  

## Outputs
The list of outputs this template exposes:

### AccountId 
  
