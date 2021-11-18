# product.template
# Description
Builds out a public subnet for use


## Parameters
The list of parameters for this template:

### VPCId 
Type: String  
Description: VPC to create the subnet in
 
### PublicSubnetCIDR 
Type: String 
Default: 10.0.0.0/16 
Description: CIDR to use for the Public Subnet
 

## Resources
The list of resources this template creates:

### PublicSubnet 
Type: AWS::EC2::Subnet 
Description: The public subnet that is created 
### InternetGateway 
Type: AWS::EC2::InternetGateway 
Description: The internet gateway to attach to the public subnet 
### GatewayAttachement 
Type: AWS::EC2::VPCGatewayAttachment 
Description: Attach the gateway to the subnet 
### PublicRouteTable 
Type: AWS::EC2::RouteTable 
Description: Associate the route table for the subnet 
### PublicRoute 
Type: AWS::EC2::Route 
Description: Set up the route out to the internet 
### PublicSubnetRouteTableAssociation 
Type: AWS::EC2::SubnetRouteTableAssociation 
Description: Associate the route 

## Outputs
The list of outputs this template exposes:

### PublicSubnetId 
Description: The subnet id of the public subnet created  

