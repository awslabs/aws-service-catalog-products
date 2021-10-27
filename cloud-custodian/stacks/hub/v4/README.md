# product.template
# Description
Resources needed for custodian hub account
{"framework": "servicecatalog-products", "role": "product", "product-set": "cloud-custodian", "product": "hub", "version": "v4"}


## Parameters
The list of parameters for this template:

### AWSOrgID 
Type: String  
Description: Organization Id for the current AWS Organization 

## Resources
The list of resources this template creates:

### EventBusPolicy 
Type: AWS::Events::EventBusPolicy 
Description: Grants perms for the given org to putevents 

## Outputs
The list of outputs this template exposes:

