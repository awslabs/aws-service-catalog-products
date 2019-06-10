# product.template
# Description
account-bootstrap-shared-product and account-creation-shared-product must both be provisioned into the same account
before this will work - they build some resources needed for this to work and they provision the SSM params with the
correct ARNs so this works with no copy and pasting.
Provisioning this template will create an AWS Account and bootstrap it using aws-service-catalog-puppet so you can
provision products into the account.


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
### TargetOU 
Type: String 
Default: None 
Description: OU/path where the created account should be moved to once creation is completed - None means no move 
### AccountVendingCreationLambdaArn 
Type: String 
Default: account-vending-creation-lambda 
Description: The ARN of the account creation lambda 
### AccountVendingBootstrapperLambdaArn 
Type: String 
Default: account-vending-bootstrapper-lambda 
Description: The ARN of the account bootstrapping lambda 

## Resources
The list of resources this template creates:

### Account 
Type: Custom::CustomResource 
Description: A custom resource representing an AWS Account 
### Bootstrap 
Type: Custom::CustomResource  

## Outputs
The list of outputs this template exposes:

### AccountId 
  

