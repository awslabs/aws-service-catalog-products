# product.template
# Description
Creates IAM Roles for OpsAdmin, FinOps and Security Team Members in the Account which can be assumed by Users coming from **a** Security Account. Note that the OpsAdmin role has a policy attached limiting it to only being able to launch a specific instance. This is just a reference to what you could do to avoid FULL Administrator Access.


## Parameters
The list of parameters for this template:

### SecurityAccountId 
Type: String  
Description: 12 Digit Account Number of the Security Account 

## Resources
The list of resources this template creates:

### IT-OpsAdminRole 
Type: AWS::IAM::Role   
### PolicyForAdmins 
Type: AWS::IAM::Policy  
### IT-FinOpsRole 
Type: AWS::IAM::Role  
### PolicyForFinops 
Type: AWS::IAM::Policy  
### IT-SecurityRole 
Type: AWS::IAM::Role  

## Outputs
The list of outputs this template exposes:

