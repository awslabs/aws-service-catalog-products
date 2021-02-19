# aws-control-tower-account-factory
# Description
Augments AWS Control Tower Account Factory - simplifies user input, dispatches extra parameters via AWS SNS andreturns the account id as an output
 
## Parameters
The list of parameters for this template:

### AccountName 
Type: String  
Description: The AWS Account Name 
### AccountEmail 
Type: String  
Description: The account email. This must be unique across AWS and must already exist. 
### SSOUserFirstName 
Type: String  
Description: SSO user first name. 
### SSOUserLastName 
Type: String  
Description: SSO user last name. 
### SSOUserEmail 
Type: String  
Description: SSO user email. A new SSO user will be created for this email, if it does not exist. This SSO user will be associated with the new managed Account. 
### AccountType 
Type: String  
Description: Which stage of the SDLC is the account going to be used for 
### AccountGroup 
Type: String  
Description: Which platform does the account belong to 
### GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn 
Type: String  
Description: The ARN of the lambda that converts group and type to Arn 
### GovernanceAtScaleAccountFactoryAccountDetailsCRArn 
Type: String  
Description: The ARN of the lambda that looks up account details for given account name 
### GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn 
Type: String  
Description: The ARN of the lambda that will dispatch SNS notifications on account creation / update 
### GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn 
Type: String  
Description: The ARN of the lambda that will bootstrap the created account as a spoke for SCT 

## Resources
The list of resources this template creates:

### OUDetails 
Type: Custom::Resource  
### TriggerCoreAccountFactory 
Type: AWS::ServiceCatalog::CloudFormationProvisionedProduct  
### AccountDetails 
Type: Custom::Resource  
### Notifier 
Type: Custom::Resource  
### Bootstraper 
Type: Custom::CustomResource  

## Outputs
The list of outputs this template exposes:

### AccountId 
Description: AccountId for the newly created AWS Account
  

### AccountOrganizationalUnitName 
Description: OrganizationalUnitName for the newly created AWS Account
  
## Examples

### Service Catalog Factory Portfolio
The following example demonstrates how to create the `aws-control-tower-account-factory` Service Catalog Product in your Service Catalog Factory portfolio `yaml` file
```yaml
Portfolios:
  Components:
    - Description: aws-control-tower-account-factory
      Distributor: CCOE
      Name: aws-control-tower-account-factory
      Owner: CCOE@Example.com
      Source:
        Configuration:
          RepositoryName: aws-control-tower-account-factory
        Provider: CodeCommit
      SupportDescription: Find us on Slack or Wiki
      SupportEmail: ccoe-support@Example.com
      SupportUrl: https://example.com/intranet/teams/ccoe/products/account-factory
      Tags: []
      Versions:
        - Description: Augments AWS Control Tower Account Factory - simplifies user input,
            dispatches extra parameters via AWS SNS andreturns the account id as an output
          Name: v1
          Source:
            Provider: CodeCommit
            Configuration:
              BranchName: v1
              RepositoryName: aws-control-tower-account-factory
      ProviderName: ccoe
      Tags:
        - Key: team
          Value: ccoe
```

### Service Catalog Puppet Launch
The following example demonstrates how to provision the `aws-control-tower-account-factory` Service Catalog Product in your Service Catalog Puppet `manifest.yaml` file
```yaml
launches:
  aws-control-tower-account-factory-account:
    depends_on:
      - account-type-to-organizational-unit-chooser
      - account-details
      - account-create-update-notifier
      - account-bootstrap-shared
    deploy_to:
      tags:
        - regions: default_region
          tag: scope:puppet_account
    parameters:
      AccountEmail:
        default: emailme@example.com
      AccountGroup:
        default: workloads
      AccountName:
        default: devaccountforteamx
      AccountType:
        default: dev
      GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn:
        ssm:
          name: /governance-at-scale-account-factory/account-create-update-notifier/GovernanceAtScaleAccountFactoryAccountCreateUpdateNotifierCRArn
      GovernanceAtScaleAccountFactoryAccountDetailsCRArn:
        ssm:
          name: /governance-at-scale-account-factory/account-details/GovernanceAtScaleAccountFactoryAccountDetailsCRArn
      GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn:
        ssm:
          name: /governance-at-scale-account-factory/account-type-to-organizational-unit-chooser/GovernanceAtScaleAccountFactoryAccountTypeToOUChooserCRArn
      GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn:
        ssm:
          name: /governance-at-scale-account-factory/account-bootstrap-shared/GovernanceAtScaleAccountFactoryBootstrapperProjectCustomResourceArn
      SSOUserEmail:
        default: emailme@example.com
      SSOUserFirstName:
        default: Jane
      SSOUserLastName:
        default: Doe
    portfolio: demo-central-it-team-portfolio
    product: aws-control-tower-account-factory
    version: v1
```