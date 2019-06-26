# product.template
# Description
Lambda for backing custom resources to create an AWS Account


## Parameters
The list of parameters for this template:

### AssumableRoleInRootAccountArn 
Type: String  
Description: The Arn of the role to be used to interact with AWS Orgs
 

## Resources
The list of resources this template creates:

### AccountCustomResourceRole 
Type: AWS::IAM::Role  
### AccountCustomResource 
Type: AWS::Serverless::Function 
Description: The lambda function that creates an account when called using a CloudFormation Custom Resource:
```yaml
Account:
  Type: Custom::CustomResource
  Description: A custom resource representing an AWS Account
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

### AccountCustomResourceArn 
Description: the Arn of the custom resource that can be used to create an account
  

