# account-creation-notifier-cfh-handler
# Description
This product creates an AWS Lambda as a subscription to an SNS topic. The Lambda function is used to relay messages from SNS to a custom HTTP POST endpoint
 
# Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### AccountCreateUpdateNotifierTopicArn 
*Type:* String   
*Description:* The ARN of the SNS topic to create the subscription for
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateCFHHandlerIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used for the AWS Lambda function

## Resources
The list of resources this template creates:

### Subscription
*Type:* AWS::SNS::Subscription  
*Description:* A subscription to the provided SNS topic that will trigger the **Function** AWS Lambda Function
### Permission
*Type:* AWS::Lambda::Permission  
*Desciption:* The permission that allows the provided SNS topic to invoke the **Function** AWS Lambda function
### Function 
*Type:* AWS::Lambda::Function  
*Description:* An AWS Lambda function the relays messages from the provided SNS topic to the provided HTTP POST endpoint 
### Role 
*Type:* AWS::IAM::Role  
*Description:* An IAM role used as the execution role for the **Function** AWS Lambda function
