# account-bootstrap-shared
# Description
Creates, codebuild project that can be run to bootstrap an account and lambda function that can be used to back a custom resource so the codebuild project can be started from CloudFormation
 


## Parameters
The list of parameters for this template:

### AssumableRoleArnInRootAccountForBootstrapping 
Type: String  
Description: The Arn of the assumable role from the root account 
### GovernanceAtScaleAccountFactoryIAMRolePath 
Type: String  
Description: The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountBootstrapSharedBootstrapperIAMRoleName 
Type: String  
Description: The name to use for IAM role that will be used by codebuild to bootstrap spokes 
### GovernanceAtScaleAccountFactoryAccountBootstrapSharedCustomResourceIAMRoleName 
Type: String  
Description: The name to use for IAM role that will be used by lambda to trigger a bootstrap 

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

### GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn 
Description: Outputs the BootstrapperProjectCustomResource Arn so others can use it
  
