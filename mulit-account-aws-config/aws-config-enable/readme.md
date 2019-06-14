# product.template
# Description
This template creates a Config Recorder, an Amazon S3 bucket where logs are published.
You can optionally change the behaviour:
  - which encryption to use for your buckets


## Parameters
The list of parameters for this template:

### LoggingAccountID
Type: String  
Description: This is the account where the S3 buckets should be stored. If this is the account where the template is deployed
the bucket will be created

### SecurityAccountID
Type: String  
Description: AccountID for the secrity account to deploy to aggregated SNS

### SSEAlgorithm
Type: String
Default: AES256
Description: Which S3 bucket SSE Algorithm to use for the bucket.
### KMSMasterKeyID
Type: String  
Description: KMS key ID required if ```SSEAlgorithm``` is aws:kms.
### ConfigBucketName
Type: String  
Description: The name of S3 Bucket to use for config logs
### EmailAddress
Type: String  
Description: The Email Address to forward Notifications to
### ORGID
Type: String  
Description: PrincipalOrgID to enable within the topic policy

## Resources
The list of resources this template creates:

### ConfigRecorder
Type: AWS::Config::ConfigurationRecorder  
### DeliveryChannel
Type: AWS::Config::DeliveryChannel  
### ConfigRole
Type: AWS::IAM::Role
Description: The IAM role used to configure AWS Config
### AggregatedTopic
Type: AWS::SNS::Topic
Description: SNS Topic that the org can use to send emails
### SNSPolicy
Type: AWS::SNS::TopicPolicy
Description: Allow the org to post to the topic
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
