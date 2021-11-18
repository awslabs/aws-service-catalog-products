# account-creation-notifier-cfh-handler
# Description
Lambda to back a custom resource that dispatches notifications to an included SNS Topic
 


## Parameters
The list of parameters for this template:

### AccountCreateUpdateNotifierTopicArn 
Type: String   
### GovernanceAtScaleAccountFactoryIAMRolePath 
Type: String  
Description: The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateCFHHandlerIAMRoleName 
Type: String  
Description: The name to use for IAM role that will be used for the lambda notifies CFH when accounts are created/updated
 

## Resources
The list of resources this template creates:

### Function 
Type: AWS::Lambda::Function 
Description: Lambda function to call CFH
 
### Role 
Type: AWS::IAM::Role 
Description: IAM role needed to publish account creations to SNS.
 

## Outputs
The list of outputs this template exposes:
