# account-type-to-organizational-unit-chooser
# Description
This product takes the given account type and returns the organizational unit it should be assigned to
 
## Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountTypeChooserCRIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used to list accounts for bootstrapping purposes 

## Resources
The list of resources this template creates:

### Function 
*Type:* AWS::Lambda::Function  
*Description:* An AWS Lambda function to back an AWS CloudFormation custom resource. This expects a ResourceProperty of AccountType and
will return an organizational_unit_id based on the dict organizational_unit_ids
 
### Role 
*Type:* AWS::IAM::Role  
*Description:* An IAM role that serves as the execution role for the AWS Lambda function
 

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn 
*Description:* The ARN of the AWS Lambda function
  
