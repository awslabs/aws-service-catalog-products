# govcloud-account-onboard
# Description
This product creates a Lambda function with an API Gateway endpoint. The purpose of the Lambda function is to:
1. Add a newly created GovCloud account to the GovCloud organization through an automated invitation and handshake process
2. Move the account to the correct Organizational Unit (OU)
3. Bootstrap the account as a spoke of the GovCloud Service Catalog Puppet account
 
The API Gateway provides an endpoint for the Lambda so it can be called externally from GovCloud. 

## Usage
This product is intended to be used as part of the GovCloud account creation process. It must be provisioned in the GovCloud Organization management account

## Parameters
The list of parameters for this template:

### OrganizationAccountAccessRole 
*Type:* String  
*Default:* OrganizationAccountAccessRole  
*Description:* The name of the IAM Role used for cross account assess for AWS Organizations 
### PuppetAccountAccessRoleArn 
*Type:* String  
*Default:* PuppetAccountAccessRole  
*Description:* The ARN of the IAM Role used for cross account assess for bootstrapping Puppet
### BootstrapperProjectName 
*Type:* String  
*Default:* servicecatalog-puppet-single-account-bootstrapper  
*Description:* The name of the CodeBuild project that bootstraps the member account as a spoke
### GovernanceAtScaleAccountFactoryIAMRolePath 
*Type:* String  
*Description:* The path to use for IAM roles in this template
### GovernanceAtScaleAccountFactoryAccountAccountInvitationIAMRoleName 
*Type:* String  
*Description:* The name to use for IAM role that will be used by Lambda to add an account to an organization

## Resources
The list of resources this template creates:

### AccountInvitationAPIGW 
*Type:* AWS::Serverless::Api  
*Description:* An API Gateway that is used to provide an endpoint for the **AccountInvitationFunction** AWS Lambda function
### AccountInvitationRole 
*Type:* AWS::IAM::Role  
*Description:* An IAM Role that is used as the execution role for the **AccountInvitationFunction** AWS Lambda function
### AccountInvitationFunction 
*Type:* AWS::Serverless::Function  
*Description:* An AWS Lambda function that automates adding a GovCloud account to the GovCloud organization, moving it to the correct OU and bootstrapping it as a spoke of the Puppet account
 

## Outputs
The list of outputs this template exposes:

### AccountInvitationFunctionArn 
*Description:* Outputs the AccountInvitationFunction ARN so others can use it
  
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `govcloud-account-onboard` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: govcloud-account-onboard
      Distributor: CCOE
      Name: govcloud-account-onboard
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: govcloud-account-onboard
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
        - Description: 'This product creates a Lambda function with an API Gateway endpoint. 
            The purpose of the Lambda function is to:
            1. Add a newly created GovCloud account to the GovCloud organization through an 
            automated invitation and handshake process
            2. Move the account to the correct Organizational Unit (OU)
            3. Bootstrap the account as a spoke of the GovCloud Service Catalog Puppet account'
          Name: v1
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v1
              RepositoryName: govcloud-account-onboard
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `govcloud-account-onboard` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file.
```yaml
launches:
  govcloud-account-onboard:
    parameters:
      OrganizationAccountAccessRole:
        default: OrganizationAccountAccessRole
      PuppetAccountAccessRole:
        default: PuppetAccountAccessRole
      BootstrapperProjectName:
        default: servicecatalog-puppet-single-account-bootstrapper
      GovernanceAtScaleAccountFactoryIAMRolePath:
        default: /AccountFactory-IAMRolePath/
      GovernanceAtScaleAccountFactoryAccountAccountInvitationIAMRoleName:
        default: AccountInvitationRole
    portfolio: demo-central-it-team-portfolio
    product: govcloud-account-onboard
    version: v1
    deploy_to:
      tags:
        - tag: scope:org_management
          regions: default_region
```