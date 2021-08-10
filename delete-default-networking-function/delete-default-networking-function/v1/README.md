# product.template
# Description
Deletes the following default networking components from AWS Accounts:
1) Deletes the internet gateway
2) Deletes the subnets
4) Deletes the network access lists
5) Deletes the security groups
6) Deletes the default VPC
{"framework": "servicecatalog-products", "role": "product", "product-set": "delete-default-vpc", "product": "delete-default-vpc", "version": "v1"}


## Parameters
The list of parameters for this template:

### RegionsToDeleteFrom 
Type: String  
Description: Comma separated list of AWS Regions to delete the default VPC from 

## Resources
The list of resources this template creates:

### DefaultVpcDeletionRole 
Type: AWS::IAM::Role  
### CustomDefaultVpcDeletionPolicy 
Type: AWS::IAM::Policy  
### DefaultVpcDeletionLambda 
Type: AWS::Lambda::Function  

## Outputs
The list of outputs this template exposes:

