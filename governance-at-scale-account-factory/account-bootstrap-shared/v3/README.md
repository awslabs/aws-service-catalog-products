# account-bootstrap-shared
# Description
This product creates an AWS CodeBuild project that can be run to bootstrap an account. It also includes an AWS Lambda function that can be used to back a custom resource so that the CodeBuild project can be started from AWS CloudFormation

## Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### AssumableRoleArnInRootAccountForBootstrapping 
*Type:* String  
*Description:* The ARN of the assumable role from the root account 
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountBootstrapSharedBootstrapperIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used by AWS CodeBuild to bootstrap spokes 
### GovernanceAtScaleAccountFactoryAccountBootstrapSharedCustomResourceIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used by AWS Lambda to trigger a bootstrap 

## Resources
The list of resources this template creates:

### BootstrapperRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM service role used by the **BootstrapperProject** AWS CodeBuild project
### BootstrapperProject 
*Type:* AWS::CodeBuild::Project  
*Description:* An AWS CodeBuild project that:
  - Installs `aws-service-catalog-puppet`
  - Runs `servicecatalog-puppet bootstrap-spoke-as` 
### BootstrapperProjectCustomResourceRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM Role that is used as an execution role for the **BootstrapperProjectCustomResource** Lambda function
### BootstrapperProjectCustomResource 
*Type:* AWS::Serverless::Function  
*Description:* An AWS Lambda function that runs an AWS CodeBuild project to bootstrap an account for Service Catalog Puppet. This Lambda function can be used to back a custom resource. You can get the ARN by checking the SSM Parameter
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
*Description:* Outputs the BootstrapperProjectCustomResource ARN so others can use it
  
