# govcloud-account-onboard
# Description
This product creates a Lambda function with an API Gateway endpoint. The purpose of the Lambda function is to:
1. Add a newly created GovCloud account to the GovCloud organization through an automated invitation and handshake process
2. Move the account to the correct Organizational Unit (OU)
3. Bootstrap the account as a spoke of the GovCloud Service Catalog Puppet account
 
The API Gateway provides an endpoint for the Lambda so it can be called externally from GovCloud. 

## Usage
This product is intended to be used as part of the GovCloud account creation process. It must be provisioned in the GovCloud Organization management account

## Parameters
The list of parameters for this template:

### OrganizationAccountAccessRole 
*Type:* String  
*Default:* OrganizationAccountAccessRole  
*Description:* The name of the IAM Role used for cross account assess for AWS Organizations 
### PuppetAccountAccessRole 
*Type:* String  
*Default:* PuppetAccountAccessRole  
*Description:* The name of the IAM Role used for cross account assess for bootstrapping Puppet
### BootstrapperProjectName 
*Type:* String  
*Default:* servicecatalog-puppet-single-account-bootstrapper  
*Description:* The name of the CodeBuild project that bootstraps the member account as a spoke
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template
### GovernanceAtScaleAccountFactoryAccountAccountInvitationIAMRoleName 
*Type:* String  
*Description:* The name to use for IAM role that will be used by Lambda to add an account to an organization

## Resources
The list of resources this template creates:

### AccountInvitationAPIGW 
*Type:* AWS::Serverless::Api  
*Description:* API Gateway that is used to provide an endpoint for the Lambda function
### AccountInvitationRole 
*Type:* AWS::IAM::Role  
*Description:* The Lambda execution IAM role 
### AccountInvitationFunction 
*Type:* AWS::Serverless::Function  
*Description:* The Lambda function that automates adding a GovCloud account to the GovCloud organization, moving it to the correct OU and bootstrapping it as a spoke of the Puppet account
 

## Outputs
The list of outputs this template exposes:

### AccountInvitationFunctionArn 
*Description:* Outputs the AccountInvitationFunction ARN so others can use it
  
