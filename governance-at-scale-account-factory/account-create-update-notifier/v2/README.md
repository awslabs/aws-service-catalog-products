# account-create-update-notifier
# Description
This product creates an AWS Lambda function to back a custom resource that dispatches notifications to an included SNS Topic
 
## Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateCRIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used for the AWS Lambda that backs a custom resource 

## Resources
The list of resources this template creates:

### SNSTopic 
*Type:* AWS::SNS::Topic  
*Description:* An SNS Topic others can subscribe to so that they can find out about account creations 
### Function 
*Type:* AWS::Lambda::Function  
*Description:* An AWS Lambda function to dispatch notifications to the SNSTopic 
### Role 
*Type:* AWS::IAM::Role  
*Description:* The IAM role that is needed to publish account creations to SNS
 

## Outputs
The list of outputs this template exposes:

### AccountCreateUpdateNotifierTopicArn 
*Description:* The ARN of the SNS topic  
### AccountCreateUpdateNotifierTopicName 
*Description:* The name of the SNS topic
### GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn 
*Description:* The ARN of the AWS Lambda function that can be used to back custom resources to notify others that accounts have been created
  
