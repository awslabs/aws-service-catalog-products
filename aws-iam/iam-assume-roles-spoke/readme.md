# product.template
# Description
Creates IAM Roles in the Account which can be assumed by Users coming from Security Account


## Parameters
The list of parameters for this template:

### SecurityAccountId 
Type: String  
Description: 12 Digit Account Number of the Security Account 

## Resources
The list of resources this template creates:

### opsadminrole 
Type: AWS::IAM::Role  
### breakglassrole 
Type: AWS::IAM::Role  
### enforcerrole 
Type: AWS::IAM::Role  
### developerrole 
Type: AWS::IAM::Role  
### policyForAdmins 
Type: AWS::IAM::Policy  
### customPolicyForRestrictingServiceCatalog 
Type: AWS::IAM::ManagedPolicy  
### accountownerrole 
Type: AWS::IAM::Role  
### policyForAppOwner 
Type: AWS::IAM::Policy  
### finopsrole 
Type: AWS::IAM::Role  
### policyForFinops 
Type: AWS::IAM::Policy  
### securityrole 
Type: AWS::IAM::Role  

## Outputs
The list of outputs this template exposes:

