# product.template
# Description
Creates an AWS Lambda that listens to SNS notifications and writes the payload to S3
{"version": "v2", "framework": "servicecatalog-products", "role": "product", "product-set": "governance-at-scale-account-management", "product": "account-recorder"}


## Parameters
The list of parameters for this template:

### AccountCreationSNSTopicArn 
Type: String   
### GASDataStoreBucketName 
Type: String   

## Resources
The list of resources this template creates:

### AccountRecorderRole 
Type: AWS::IAM::Role 
Description: IAM role needed to publish account creations to S3.
 
### AccountRecorder 
Type: AWS::Lambda::Function 
Description: Listens to AWS SNS and writes to AWS S3 
### AccountRecorderSNSPermission 
Type: AWS::Lambda::Permission 
Description: allow sns to trigger the lambda 
### AccountRecorderSubscription 
Type: AWS::SNS::Subscription 
Description: trigger the lambda when the sns topic is used 

## Outputs
The list of outputs this template exposes:

### AccountRecorderName 
Description: The name of the account recorder function 

### AccountRecorderArn 
Description: The Arn of the account recorder function 
