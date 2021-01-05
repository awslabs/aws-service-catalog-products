# account-creation-shared
# Description
This product creates an AWS Lambda function for backing custom resources to create an AWS Account
 
## Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn 
*Type:* String  
*Description:* The ARN of the assumable role in the organization root account that is used to interact with AWS Organizations
### OrganizationAccountAccessRole 
*Type:* String  
*Default:* OrganizationAccountAccessRole  
*Description:* The name of the IAM Role used for cross account access for AWS Organizations
### GovernanceAtScaleAccountFactoryIAMRolePath
*Type:* String  
*Description:* The path to use for IAM roles in this template

## Resources
The list of resources this template creates:

### AccountCustomResourceRole 
*Type:* AWS::IAM::Role  
*Description:* The IAM role that is used as the execution role for the **AccountCustomResource** AWS Lambda function
### AccountCustomResource 
*Type:* AWS::Serverless::Function  
*Description:* The AWS Lambda function that creates an account when called using a CloudFormation Custom Resource:
```yaml
Account:
  Type: Custom::CustomResource
  Description: A custom resource representing an AWS Account
  Properties:
    ServiceToken: !Ref AccountVendingCreationLambda
    Email: !Ref Email
    AccountName: !Ref AccountName
    IamUserAccessToBilling: !Ref IamUserAccessToBilling
    TargetOU: !Ref TargetOU
```
 

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountCreationCRArn 
*Description:* the ARN of the custom resource that can be used to create an account
  
