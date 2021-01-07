# account-creation-shared
# Description
This product creates an AWS Lambda function for backing custom resources to create an AWS Account
 
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
*Description:* The name of the IAM Role used for cross account access for AWS Organizations
### GovernanceAtScaleAccountFactoryIAMRolePath
*Type:* String  
*Description:* The path to use for IAM roles in this template

## Resources
The list of resources this template creates:

### AccountCustomResourceRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM role that is used as the execution role for the **AccountCustomResource** AWS Lambda function
### AccountCustomResource 
*Type:* AWS::Serverless::Function  
*Description:* An AWS Lambda function that creates an account when called using a CloudFormation Custom Resource:
```yaml
Account:
  Type: Custom::CustomResource
  Description: A custom resource representing an AWS Account
  Properties:
    ServiceToken: !Ref AccountVendingCreationLambda
    Email: !Ref Email
    AccountName: !Ref AccountName
    IamUserAccessToBilling: !Ref IamUserAccessToBilling
    TargetOU: !Ref TargetOU
```
 

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountCreationCRArn 
*Description:* the ARN of the custom resource that can be used to create an account
  
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-creation-shared` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-creation-shared
      Distributor: CCOE
      Name: account-creation-shared
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-creation-shared
        Provider: CodeCommit
      BuildSpec: |
        version: 0.2
        phases:
          install:
            runtime-versions:
              python: 3.8
          build:
            commands:
              - pip install -r requirements.txt -t src
            {% for region in ALL_REGIONS %}
              - aws cloudformation package --template $(pwd)/product.template.yaml --s3-bucket sc-factory-artifacts-${ACCOUNT_ID}-{{ region }} --s3-prefix ${STACK_NAME} --output-template-file product.template-{{ region }}.yaml
            {% endfor %}
        artifacts:
          files:
            - '*'
            - '**/*'
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Tags: []
      Versions:
        - Description: This product creates an AWS Lambda function for backing custom 
            resources to create an AWS Account
          Name: v4
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v5
              RepositoryName: account-creation-shared
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-creation-shared` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-creation-shared:
    depends_on:
      - account-creation-shared-org-bootstrap
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:puppet_account
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/account-creation-shared/GovernanceAtScaleAccountFactoryAccountCreationCRArn
          stack_output: GovernanceAtScaleAccountFactoryAccountCreationCRArn
    parameters:
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
      GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn:
        ssm:
          name: /governance-at-scale-account-factory/account-creation-shared-org-bootstrap/GovernanceAtScaleAccountFactoryAccountCreationSharedOrgRoleArn
      OrganizationAccountAccessRole:
        default: OrganizationAccountAccessRole
    portfolio: demo-central-it-team-portfolio
    product: account-creation-shared
    version: v5
```