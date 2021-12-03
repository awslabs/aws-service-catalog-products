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
### OAdminTeamGroupName 
Type: String 
Default: OSSAdminTeam 
Description: Name of the Security Team Group 

## Resources
The list of resources this template creates:

### IT-AdminGroup 
Type: AWS::IAM::Group  
### IT-FinOpsGroup 
Type: AWS::IAM::Group  
### IT-SecurityTeamGroup 
Type: AWS::IAM::Group  

## Outputs
The list of outputs this template exposes:

None

