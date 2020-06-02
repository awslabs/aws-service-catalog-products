# product.template
# Description
Creates the datastore needed for governance@scale account management
{"version": "v1", "framework": "servicecatalog-products", "role": "product", "product-set": "governance-at-scale-account-management", "product": "datastore"}

## Parameters
The list of parameters for this template:

## Resources
The list of resources this template creates:

### Account 
Type: AWS::S3::Bucket 
Description: Storage for the account management apis 

## Outputs
The list of outputs this template exposes:

### GASDataStoreBucketName 
Description: The name of the bucket 

### GASDataStoreBucketArn 
Description: The Arn of the bucket 
