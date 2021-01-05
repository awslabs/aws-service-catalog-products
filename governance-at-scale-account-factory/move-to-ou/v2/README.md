# account-creation-shared
# Description
This product creates an AWS Lambda function that is used to move an AWS account to specified organizational unit (OU)
 
## Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn 
*Type:* String  
*Description:* The ARN of the IAM role in the organization root that can be assumed and used to interact with AWS Organizations 
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template

## Resources
The list of resources this template creates:

### MoveToOUCustomResourceRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM role that is used as a execution role for the **MoveToOUCustomResource** AWS Lambda function
### MoveToOUCustomResource 
*Type:* AWS::Serverless::Function  
*Description:* An AWS Lambda function that moves an account into the provided organizational unit (OU):
```yaml
MoveToOU:
  Type: Custom::Resource
  Description: A custom resource for moving an account to an OU
  Properties:
    ServiceToken: !Ref GovernanceAtScaleAccountFactoryMoveToOUArn
    AccountType: !Ref AccountType
    AccountGroup: !Ref AccountGroup
    TargetOU: !GetAtt OUDetails.OrganizationalUnitName
    AccountId: !GetAtt Account.account_id
```

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryMoveToOUCRArn 
*Description:* The ARN of the **MoveToOUCustomResource** AWS Lambda function that can be used to move an account to an OU
  
