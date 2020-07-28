# product.template
# Description
Creates:
 - codebuild project that can be run to bootstrap an account
 - lambda function that can be used to back a custom resource so the codebuild project can be started from CloudFormation


## Parameters
The list of parameters for this template:


## Resources
The list of resources this template creates:

### BootstrapperRole 
Type: AWS::IAM::Role  
### BootstrapperProject 
Type: AWS::CodeBuild::Project 
Description: Wrapper project that:
  - installs aws-service-catalog-puppet
  - runs bootstrap-spoke-as
 
### BootstrapperProjectCustomResourceRole 
Type: AWS::IAM::Role  
### BootstrapperProjectCustomResource 
Type: AWS::Serverless::Function 
Description: Lambda function that can be used to back a custom resource.  You can get the ARN by checking the SSM Parameter
```account-vending-bootstrapper-lambda```:
```yaml
Account:
  Type: Custom::CustomResource
  Properties:
    ServiceToken: !Ref AccountVendingCreationLambda
    Email: !Ref Email
    AccountName: !Ref AccountName
    OrganizationAccountAccessRole: !Ref OrganizationAccountAccessRole
    IamUserAccessToBilling: !Ref IamUserAccessToBilling
    TargetOU: !Ref TargetOU
```
 

## Outputs
The list of outputs this template exposes:

### BootstrapperProjectCustomResourceArn 
Description: Outputs the BootstrapperProjectCustomResource Arn so others can use it
  

