# product.template
# Description
Resourceses needed in spoke account for cloudcustodian
{"framework": "servicecatalog-products", "role": "product", "product-set": "cloud-custodian", "product": "event-forwarding", "version": "v1"}


## Parameters
The list of parameters for this template:

### CloudCustodianSpokeIAMRolePath 
Type: String 
Default: /  
### CloudCustodianHubAccountId 
Type: String   
### EnableLogFileValidation 
Type: String  
Description: Specifies whether log file validation is enabled 
### CloudCustodianHubEventBusName 
Type: String 
Default: default 
Description: The arn of the event bus from the hub account where c7n policies are deployed 
### CloudCustodianRuleForwarderIAMRoleName 
Type: String 
Default: CloudCustodianRuleForwarder 
Description: The name of the IAM service role that will put events 

## Resources
The list of resources this template creates:

### TrailBucket 
Type: AWS::S3::Bucket  
### TrailBucketPolicy 
Type: AWS::S3::BucketPolicy  
### Trail 
Type: AWS::CloudTrail::Trail  
### ForwarderRuleRole 
Type: AWS::IAM::Role 
Description: Service IAM Role to be used when triggering the event rule 
### ForwarderRule 
Type: AWS::Events::Rule  

## Outputs
The list of outputs this template exposes:

### CustodianRoleName 
Description: Name of the IAM role to be used by the hub account  

### CustodianRoleArn 
Description: Arn of the IAM role to be used by the hub account  

### TrailBucketName 
Description: Name of the s3 bucket the trail is delivering logs to  

