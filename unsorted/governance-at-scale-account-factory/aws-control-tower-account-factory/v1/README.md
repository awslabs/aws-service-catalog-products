# aws-control-tower-account-factory
# Description
Augments AWS Control Tower Account Factory - simplifies user input, dispatches extra parameters via AWS SNS andreturns the account id as an output
 


## Parameters
The list of parameters for this template:

### AccountName 
Type: String  
Description: The AWS Account Name 
### AccountEmail 
Type: String  
Description: The account email. This must be unique across AWS and must already exist. 
### SSOUserFirstName 
Type: String  
Description: SSO user first name. 
### SSOUserLastName 
Type: String  
Description: SSO user last name. 
### SSOUserEmail 
Type: String  
Description: SSO user email. A new SSO user will be created for this email, if it does not exist. This SSO user will be associated with the new managed Account. 
### AccountType 
Type: String  
Description: Which stage of the SDLC is the account going to be used for 
### AccountGroup 
Type: String  
Description: Which platform does the account belong to 
### GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn 
Type: String  
Description: The ARN of the lambda that converts group and type to Arn 
### GovernanceAtScaleAccountFactoryAccountDetailsCRArn 
Type: String  
Description: The ARN of the lambda that looks up account details for given account name 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn 
Type: String  
Description: The ARN of the lambda that will dispatch SNS notifications on account creation / update 
### GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn 
Type: String  
Description: The ARN of the lambda that will bootstrap the created account as a spoke for SCT 

## Resources
The list of resources this template creates:

### OUDetails 
Type: Custom::Resource  
### TriggerCoreAccountFactory 
Type: AWS::ServiceCatalog::CloudFormationProvisionedProduct  
### AccountDetails 
Type: Custom::Resource  
### Notifier 
Type: Custom::Resource  
### Bootstraper 
Type: Custom::CustomResource  

## Outputs
The list of outputs this template exposes:

### AccountId 
Description: AccountId for the newly created AWS Account
  

### AccountOrganizationalUnitName 
Description: OrganizationalUnitName for the newly created AWS Account
  
