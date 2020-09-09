# account-create-update-notifier
# Description
Lambda to back a custom resource that dispatches notifications to an included SNS Topic
 


## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryIAMRolePath 
Type: String  
Description: The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateCRIAMRoleName 
Type: String  
Description: The name to use for IAM role that will be used for the lambda that backs a custom resource 

## Resources
The list of resources this template creates:

### SNSTopic 
Type: AWS::SNS::Topic 
Description: SNS Topic others can subscribe to so that they can find out about account creations 
### Function 
Type: AWS::Lambda::Function 
Description: Lambda function to dispatch notifications to the SNSTopic
 
### Role 
Type: AWS::IAM::Role 
Description: IAM role needed to publish account creations to SNS.
 

## Outputs
The list of outputs this template exposes:

### AccountCreateUpdateNotifierTopicArn 
Description: Outputs the SNS topic
  

### AccountCreateUpdateNotifierTopicName 
Description: Outputs the SNS topic name
  

### GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn 
Description: Arn of lambda that can be used to back custom resources to notify others that accounts have been created
  
