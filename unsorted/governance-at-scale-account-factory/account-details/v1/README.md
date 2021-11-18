# account-details
# Description
Takes the given 'AccountName' and returns the account details
 


## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryAccountDetailsOrgRoleArn 
Type: String  
Description: AWS IAM Role in the Organizations root account that is assumable from the account where this is provisoned
 
### GovernanceAtScaleAccountFactoryIAMRolePath 
Type: String  
Description: The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountDetailsCRIAMRoleName 
Type: String  
Description: The name to use for IAM role that will be used for lambda when backing the account details custom resource 

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

### GovernanceAtScaleAccountFactoryAccountDetailsCRArn 
Description: Outputs the Function Arn so others can use it
  
