# org-bootstrap.template
# Description
IAM Role needed to use AWS Organizations to create AWS Accounts.

## Parameters
The list of parameters for this template:

### ServiceCatalogFactoryAccountId 
Type: String  
Description: The account you will be installing AWS Service Catalog Factory into 

## Resources
The list of resources this template creates:

### AssumableRoleInRootAccount 
Type: AWS::IAM::Role 
Description: IAM Role needed by the account vending machine so it can create and move accounts
 

## Outputs
The list of outputs this template exposes:

### AssumableRoleInRootAccountArn 
Description: The ARN for your Assumable role in root account  

