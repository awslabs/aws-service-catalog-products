# account-waiter
# Description
This product creates an AWS Lambda function for backing custom resources that will wait for CodeBuild and CloudFormation to become available in a newly created account
 
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
*Description:* The name of the the IAM Role used for cross account assess for AWS Organizations
### GovernanceAtScaleAccountFactoryIAMRolePath
*Type:* String  
*Description:* The path to use for IAM roles in this template
### ServiceCatalogPuppetVersion
*Type:* String  
*Description:* The version of Service Catalog Puppet in use

## Resources
The list of resources this template creates:

### AccountWaiterCustomResourceRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM role that is used as the execution role for the **AccountWaiterCustomResource** AWS Lambda function
### AccountWaiterCustomResource 
*Type:* AWS::Serverless::Function  
*Description:* An AWS Lambda function that starts an AWS CodeBuild project used to wait for CodeBuild and CloudFormation to become available in a newly created account
```yaml
AccountWaiter1:
  Type: Custom::Resource
  Description: A custom resource for waiting for an account to become active
  Properties:
    ServiceToken: !Ref GovernanceAtScaleAccountFactoryAccountWaiterArn
    AccountId: !GetAtt Account.account_id
    ServiceCatalogPuppetVersion: !Ref ServiceCatalogPuppetVersion
    Handle: !Ref AccountWaiterConditionHandle1
```
### AccountWaiterCodeBuildProjectRole
*Type:* AWS::IAM::Role  
*Description:* An IAM role that is assigned to the **AccountWaiterCodeBuildProject** AWS CodeBuild project
### AccountWaiterCodeBuildProject
*Type:* AWS::CodeBuild::Project  
*Description:* An AWS CodeBuild project used to wait for an account to become active with CodeBuild and CloudFormation available

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountWaiterCRArn 
*Description:* the ARN of the custom resource that can be used to wait for CodeBuild and CloudFormation to become active in a newly created account
  
