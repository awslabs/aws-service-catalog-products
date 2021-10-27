# account-type-to-organizational-unit-chooser
# Description
Takes the given account type and returns the organizational unit it should be assigned to
 


## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryIAMRolePath 
Type: String  
Description: The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountTypeChooserCRIAMRoleName 
Type: String  
Description: The name to use for IAM role that will be used to list accounts for bootstrapping purposes 

## Resources
The list of resources this template creates:

### Function 
Type: AWS::Lambda::Function 
Description: Lambda function to back an AWS CloudFormation custom resource.  This expects a ResourceProperty of AccountType and
will return an organizational_unit_id based on the dict organizational_unit_ids
 
### Role 
Type: AWS::IAM::Role 
Description: IAM role needed to execute account-type-to-organizational-unit-id.  Only needs basic access.
 

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn 
Description: Outputs the Function Arn so others can use it
  
