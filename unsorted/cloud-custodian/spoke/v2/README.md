# product.template
# Description
Resourceses needed in spoke account for cloudcustodian


## Parameters
The list of parameters for this template:

### CloudCustodianSpokeIAMRoleName 
Type: String 
Default: Custodian  
### CloudCustodianSpokeIAMRolePath 
Type: String 
Default: /  
### CloudCustodianHubAccountId 
Type: String   

## Resources
The list of resources this template creates:

### CustodianRole 
Type: AWS::IAM::Role 
Description: IAM Role to be assumed by the hub account for c7n to function 

## Outputs
The list of outputs this template exposes:

### CustodianRoleName 
Description: Name of the IAM role to be used by the hub account  

### CustodianRoleArn 
Description: Arn of the IAM role to be used by the hub account  

