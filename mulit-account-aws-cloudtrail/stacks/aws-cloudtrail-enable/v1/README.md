# product.template
# Description
This template creates an AWS CloudTrail trail and an Amazon S3 bucket where logs are published.
You can optionally change the behaviour:
  - which encryption to use for your buckets
  - whether CloudTrail validates the integrity of the log files
  - whether the trail is publishing events from global services, such as IAM, to the log files
  - whether the CloudTrail trail is created in the region in which you create the stack or in all regions


## Parameters
The list of parameters for this template:

### EnableLogFileValidation 
Type: String 
Default: true 
Description: Indicates whether CloudTrail validates the integrity of log files 
### IncludeGlobalEvents 
Type: String 
Default: true 
Description: Indicates whether the trail is publishing events from global services, such as IAM, to the log files. 
### MultiRegion 
Type: String 
Default: false 
Description: Indicates whether the CloudTrail trail is created in the region in which you create the stack (false) or in all
regions (true).
 
### TrailBucket 
Type: String  
Description: Bucket name for logs. 
### LoggingAccountID 
Type: String  
Description: This is the account where the S3 buckets should be stored. If this is the account where the template is deployed
the bucket will be created
 
### SSEAlgorithm 
Type: String 
Default: AES256 
Description: Which S3 bucket SSE Algorithm to use when creating the logging bucket. 
### KMSMasterKeyID 
Type: String  
Description: KMS key ID to use when SSE algorithm is aws:kms. 

## Resources
The list of resources this template creates:

### KMSTrail 
Type: AWS::CloudTrail::Trail 
Description: CloudTrail trail to use when KMS encryption is used 
### AES256Trail 
Type: AWS::CloudTrail::Trail 
Description: CloudTrail trail to use when AES256 encryption is used 
### SpokeTrail 
Type: AWS::CloudTrail::Trail 
Description: CloudTrail trail to use when deploying into a spoke account 
### S3KmsLoggingBucket 
Type: AWS::S3::Bucket 
Description: S3 bucket to use for logging the logging bucket when KMS encryption is used 
### S3KmsBucket 
Type: AWS::S3::Bucket 
Description: S3 bucket to use when KMS encryption is used for logging 
### S3KmsBucketPolicy 
Type: AWS::S3::BucketPolicy 
Description: S3 bucket policy to use when KMS encryption is used for logging 
### S3LoggingBucket 
Type: AWS::S3::Bucket 
Description: S3 bucket to use for logging the logging bucket when AES256 encryption is used 
### S3Bucket 
Type: AWS::S3::Bucket 
Description: S3 bucket to use when KMS encryption is used for logging 
### S3BucketPolicy 
Type: AWS::S3::BucketPolicy 
Description: S3 bucket policy to use when AES256 encryption is used for logging 

## Outputs
The list of outputs this template exposes:

