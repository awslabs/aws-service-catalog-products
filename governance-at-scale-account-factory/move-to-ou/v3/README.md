# move-to-ou
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
  
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `move-to-ou` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: move-to-ou
      Distributor: CCOE
      Name: move-to-ou
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: move-to-ou
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Versions:
        - Description: This product creates an AWS Lambda function that is used to move an 
            AWS account to specified organizational unit (OU)
          Name: v2
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v2
              RepositoryName: move-to-ou
      ProviderName: ccoe
      Tags:
        - Key: team
          Value: ccoe
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `move-to-ou` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file.
```yaml
launches:
  move-to-ou:
    depends_on:
      - account-creation-shared-org-bootstrap
    deploy_to:
      tags:
        - regions: default_region
          tag: role:puppethub
    parameters:
      GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn:
        ssm:
          name: /governance-at-scale-account-factory/account-creation-shared-org-bootstrap/GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/move-to-ou/GovernanceAtScaleAccountFactoryMoveToOUCRArn
          stack_output: GovernanceAtScaleAccountFactoryMoveToOUCRArn
    portfolio: example-account-vending-account-vending
    product: move-to-ou
    version: v2
```