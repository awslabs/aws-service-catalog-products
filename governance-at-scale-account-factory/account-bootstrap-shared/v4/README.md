# account-bootstrap-shared
# Description
This product creates an AWS CodeBuild project that can be run to bootstrap an account. It also includes an AWS Lambda function that can be used to back a custom resource so that the CodeBuild project can be started from AWS CloudFormation

## Usage
This product should be provisioned in your Service Catalog Puppet account

## Parameters
The list of parameters for this template:

### AssumableRoleArnInRootAccountForBootstrapping 
*Type:* String  
*Description:* The ARN of the assumable role from the root account 
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template 
### GovernanceAtScaleAccountFactoryAccountBootstrapSharedBootstrapperIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used by AWS CodeBuild to bootstrap spokes 
### GovernanceAtScaleAccountFactoryAccountBootstrapSharedCustomResourceIAMRoleName 
*Type:* String  
*Description:* The name to use for the IAM role that will be used by AWS Lambda to trigger a bootstrap 

## Resources
The list of resources this template creates:

### BootstrapperRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM service role used by the **BootstrapperProject** AWS CodeBuild project
### BootstrapperProject 
*Type:* AWS::CodeBuild::Project  
*Description:* An AWS CodeBuild project that:
  - Installs `aws-service-catalog-puppet`
  - Runs `servicecatalog-puppet bootstrap-spoke-as` 
### BootstrapperProjectCustomResourceRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM Role that is used as an execution role for the **BootstrapperProjectCustomResource** Lambda function
### BootstrapperProjectCustomResource 
*Type:* AWS::Serverless::Function  
*Description:* An AWS Lambda function that runs an AWS CodeBuild project to bootstrap an account for Service Catalog Puppet. This Lambda function can be used to back a custom resource. You can get the ARN by checking the SSM Parameter
```account-vending-bootstrapper-lambda```:
```yaml
Account:
  Type: Custom::CustomResource
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

### GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn 
*Description:* Outputs the BootstrapperProjectCustomResource ARN so others can use it
  
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `account-bootstrap-shared` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: account-bootstrap-shared
      Distributor: CCOE
      Name: account-bootstrap-shared
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: account-bootstrap-shared
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
        - Description: This product creates an AWS CodeBuild project that can be run to bootstrap an account. 
            It also includes an AWS Lambda function that can be used to back a custom resource 
            so that the CodeBuild project can be started from AWS CloudFormation
          Name: v3
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v3
              RepositoryName: account-bootstrap-shared
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `account-bootstrap-shared` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  account-bootstrap-shared:
    depends_on:
      - account-bootstrap-shared-org-bootstrap
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:puppet_account
    outputs:
      ssm:
        - param_name: /governance-at-scale-account-factory/account-bootstrap-shared/GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn
          stack_output: GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn
    parameters:
      AssumableRoleArnInRootAccountForBootstrapping:
        ssm:
          name: /governance-at-scale-account-factory/account-bootstrap-shared-org-bootstrap/AssumableRoleArnInRootAccountForBootstrapping
      GovernanceAtScaleAccountFactoryAccountBootstrapSharedBootstrapperIAMRoleName:
        default: AccountBootstrapSharedBootstrapperIAMRoleName
      GovernanceAtScaleAccountFactoryAccountBootstrapSharedCustomResourceIAMRoleName:
        default: AccountBootstrapSharedCustomResourceIAMRoleName
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactoryIAMRolePath/
    portfolio: demo-central-it-team-portfolio
    product: account-bootstrap-shared
    version: v3
```