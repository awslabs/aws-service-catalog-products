# account-waiter
# Description
This product creates an AWS Lambda function for backing custom resources that will wait for CodeBuild and CloudFormation to become available in a newly created account
 
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
*Description:* The name of the the IAM Role used for cross account assess for AWS Organizations
### GovernanceAtScaleAccountFactoryIAMRolePath
*Type:* String  
*Description:* The path to use for IAM roles in this template
### ServiceCatalogPuppetVersion
*Type:* String  
*Description:* The version of Service Catalog Puppet in use

## Resources
The list of resources this template creates:

### AccountWaiterCustomResourceRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM role that is used as the execution role for the **AccountWaiterCustomResource** AWS Lambda function
### AccountWaiterCustomResource 
*Type:* AWS::Serverless::Function  
*Description:* An AWS Lambda function that starts an AWS CodeBuild project used to wait for CodeBuild and CloudFormation to become available in a newly created account
```yaml
AccountWaiter1:
  Type: Custom::Resource
  Description: A custom resource for waiting for an account to become active
  Properties:
    ServiceToken: !Ref GovernanceAtScaleAccountFactoryAccountWaiterArn
    AccountId: !GetAtt Account.account_id
    ServiceCatalogPuppetVersion: !Ref ServiceCatalogPuppetVersion
    Handle: !Ref AccountWaiterConditionHandle1
```
### AccountWaiterCodeBuildProjectRole
*Type:* AWS::IAM::Role  
*Description:* An IAM role that is assigned to the **AccountWaiterCodeBuildProject** AWS CodeBuild project
### AccountWaiterCodeBuildProject
*Type:* AWS::CodeBuild::Project  
*Description:* An AWS CodeBuild project used to wait for an account to become active with CodeBuild and CloudFormation available

## Outputs
The list of outputs this template exposes:

### GovernanceAtScaleAccountFactoryAccountWaiterCRArn 
*Description:* The ARN of the custom resource that can be used to wait for CodeBuild and CloudFormation to become active in a newly created account
  
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-waiter` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-waiter
      Distributor: CCOE
      Name: account-waiter
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-waiter
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
      Versions:
        - Description: This product creates an AWS Lambda function for backing custom 
            resources that will wait for CodeBuild and CloudFormation to become 
            available in a newly created account
          Name: v4
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v4
              RepositoryName: account-waiter
      ProviderName: ccoe
      Tags:
        - Key: team
          Value: ccoe
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-waiter` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-waiter:
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
      ServiceCatalogPuppetVersion:
        default: 0.91.0
      OrganizationAccountAccessRole:
        default: OrganizationAccountAccessRole
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/account-waiter/GovernanceAtScaleAccountFactoryAccountWaiterCRArn
          stack_output: GovernanceAtScaleAccountFactoryAccountWaiterCRArn
    portfolio: example-account-vending-account-vending
    product: account-waiter
    version: v4
```