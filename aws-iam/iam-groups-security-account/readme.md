# product.template
# Description
Creates the IAM Groups in the security Account


## Parameters
The list of parameters for this template:

### FinOpsGroupName 
Type: String 
Default: FinOpsGroup 
Description: Name of the FinOps 
### SecurityTeamGroupName 
Type: String 
Default: SecurityTeamGroup 
Description: Name of the Security Team Group 
### OSSAdminTeamGroupName 
Type: String 
Default: OSSAdminTeam 
Description: Name of the Security Team Group 

## Resources
The list of resources this template creates:

### OSSAdminGroup 
Type: AWS::IAM::Group  
### FinOpsGroup 
Type: AWS::IAM::Group  
### SecurityTeamGroup 
Type: AWS::IAM::Group  

## Outputs
The list of outputs this template exposes:

