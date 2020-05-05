# product.template
# Description
Augments AWS Control Tower Account Factory - simplifies user input, dispatches extra parameters via AWS SNS and
returns the account id as an output


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

## Outputs
The list of outputs this template exposes:

### AccountId 
Description: AccountId for the newly created AWS Account

