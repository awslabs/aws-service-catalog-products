# product.template
# Description
Takes the given 'AccountName' and returns the account details


## Parameters
The list of parameters for this template:

### AssumableRoleInRootAccountArn 
Type: String  
Description: AWS IAM Role in the Organizations root account that is assumable from the account where this is provisoned
 

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

### AccountDetailsToAWSAccountIdCustomResourceArn 
Description: Outputs the Function Arn so others can use it
