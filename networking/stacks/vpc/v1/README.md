# product.template
# Description
Builds out a VPC for use


## Parameters
The list of parameters for this template:

### VPCCIDR 
Type: String 
Default: 10.0.0.0/16 
Description: Subnet to use for the VPC
 

## Resources
The list of resources this template creates:

### VPC 
Type: AWS::EC2::VPC 
Description: The vpc being created 

## Outputs
The list of outputs this template exposes:

### VPCId 
Description: The ID of the VPC that was created  

