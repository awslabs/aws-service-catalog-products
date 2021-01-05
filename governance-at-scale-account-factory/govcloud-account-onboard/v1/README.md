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
_Type:_ String  
_Default:_ OrganizationAccountAccessRole  
_Description:_ The name of the IAM Role used for cross account assess for AWS Organizations 
### PuppetAccountAccessRole 
_Type:_ String  
_Default:_ PuppetAccountAccessRole  
_Description:_ The name of the IAM Role used for cross account assess for bootstrapping Puppet
### BootstrapperProjectName 
_Type:_ String  
_Default:_ servicecatalog-puppet-single-account-bootstrapper  
_Description:_ The name of the CodeBuild project that bootstraps the member account as a spoke
### GovernanceAtScaleAccountFactoryIAMRolePath 
_Type:_ String  
_Description:_ The path to use for IAM roles in this template
### GovernanceAtScaleAccountFactoryAccountAccountInvitationIAMRoleName 
_Type:_ String  
_Description:_ The name to use for IAM role that will be used by Lambda to add an account to an organization

## Resources
The list of resources this template creates:

### AccountInvitationAPIGW 
_Type:_ AWS::Serverless::Api  
_Description:_ API Gateway that is used to provide an endpoint for the Lambda function
### AccountInvitationRole 
_Type:_ AWS::IAM::Role  
_Description:_ The Lambda execution IAM role 
### AccountInvitationFunction 
_Type:_ AWS::Serverless::Function  
_Description:_ The Lambda function that automates adding a GovCloud account to the GovCloud organization, moving it to the correct OU and bootstrapping it as a spoke of the Puppet account
 

## Outputs
The list of outputs this template exposes:

### AccountInvitationFunctionArn 
_Description:_ Outputs the AccountInvitationFunction ARN so others can use it
  
