# Account Vending
This solution is to be deployed using the service catalog tools.  Once deployed it will allow you to create new AWS
accounts using the AWS Organizations API or via the AWS Control Tower Account Factory (using AWS Service Catalog).

## Setting up
Before you can create accounts you will need to provision stacks in the stacks directory.  To create accounts you will
need to provision the products in the portfolios directory.

### Setting up the stacks
Before provisioning the stacks you will need to create pipelines for them.  To do this copy the 
stacks/account-vending.yaml file into the stacks directory of your ServiceCatalogFactory git repo.  It should look like
this:

```
tree ServiceCatalogFactory
ServiceCatalogFactory
└── stacks
    └── account-vending.yaml
```

You will most likely have other files in the repository - this is okay.

Once you have copied the file edit it to declare where your source code will be. The account-vending.yaml file uses 
paths for the source code.  You do not have to do so and are free to change it.  You can read more about 
paths / monorepos here: https://service-catalog-tools-workshop.com/every-day-use/using-a-mono-repo.html

Once you have done that you should upload/create the source code for the four stacks where ever you decided.

Once you have done that you can commit and push your ServiceCatalogFactory changes and the solution will execute.  Once
completed you will have four new pipelines that will run creating artefacts for the four stacks:

- prereqs-puppet-account
- prereqs-controltower-account
- prereqs-orgs-account
- prereqs-puppet-account-optional

### Creating the Service Catalog Products

This is very similar to the creating of the stacks.  You will need to copy the portfolios/account-vending.yaml file
into the portfolios directory of your ServiceCatalogFactory repository.  Within the portfolios/account-vending.yaml file
you will need to update the source details to declare where your source code will be.  This works the same as stacks.

You will need to upload/create the source code for the two products where ever you decided.

Once you have done that you can commit and push your ServiceCatalogFactory changes and the solution will execute.  Once
completed you will have four new pipelines that will run creating artefacts for the two products:

account-vending-with-aws-organizations
account-vending-with-aws-control-tower

You can verify this by checking Service Catalog to see the products are there.


## Provisioning the stacks

When accounts are created using AWS Service Catalog or AWS Control Tower this solution will ensure we wait for the 
account to be created, then bootstrap it and then run the single account pipeline for it.  This will ensure it is ready 
for use by the end user.

To do all of this there is a step function and some helper lambda functions.  To ensure they are provisioned you will
need to provision the stacks we created in the earlier step.  To provision the stacks you will need to add the following
to your manifest file:

```yaml
parameters:
  AccountVendingIAMRolesPath:
      default: /foundational/account-vending/
stacks:
  account-vending-prereqs-controltower-account:
    name: account-vending-prereqs-controltower-account
    version: v1
    execution: hub
    capabilities:
      - CAPABILITY_NAMED_IAM
    parameters:
      AccountVendingControlTowerRoleName:
        default: AccountVendingOrgsRole
    deploy_to:
      tags:
        - tag: 'role:controltower_management'
          regions: default_region
    outputs:
      ssm:
        - param_name: "/foundational/account-vending/AccountVendingAccountVendingControlTowerRoleArn"
          stack_output: AccountVendingAccountVendingControlTowerRoleArn

  account-vending-prereqs-orgs-account:
    name: account-vending-prereqs-orgs-account
    version: v1
    execution: hub
    capabilities:
      - CAPABILITY_NAMED_IAM
    parameters:
      AccountVendingOrgsRoleName:
        default: AccountVendingOrgsRoleName
      AWSOrganizationsCrossAccountRoleName:
        default: OrganizationAccountAccessRole
    deploy_to:
      tags:
        - tag: 'role:orgs_management'
          regions: default_region
    outputs:
      ssm:
        - param_name: "/foundational/account-vending/AccountVendingOrgsRoleArn"
          stack_output: AccountVendingOrgsRoleArn

  account-vending-prereqs-puppet-account-optional:
    name: account-vending-prereqs-puppet-account-optional
    version: v1
    execution: hub
    parameters:
      AccountVendingAccountNotificationCreatedTopicName:
        default: AccountVendingAccountNotificationCreatedTopic
    deploy_to:
      tags:
        - tag: 'role:sct'
          regions: default_region
    outputs:
      ssm:
        - param_name: "/foundational/account-vending/AccountVendingAccountNotificationCreatedTopicArn"
          stack_output: AccountVendingAccountNotificationCreatedTopicArn

  account-vending-prereqs-puppet-account:
    name: account-vending-prereqs-puppet-account
    version: v1
    execution: hub
    capabilities:
      - CAPABILITY_NAMED_IAM
      - CAPABILITY_AUTO_EXPAND
    depends_on:
      - name: account-vending-prereqs-controltower-account
        affinity: stack
        type: stack
      - name: account-vending-prereqs-orgs-account
        affinity: stack
        type: stack
      - name: account-vending-prereqs-puppet-account-optional
        affinity: stack
        type: stack
    parameters:
      AccountVendingIAMRolesPath:
        default: /foundational/account-vending/
      AccountVendingAccountOrganizationsRoleArn:
        ssm:
          name: "/foundational/account-vending/AccountVendingOrgsRoleArn"
      AccountVendingControlTowerRoleArn:
        ssm:
          name: "/foundational/account-vending/AccountVendingAccountVendingControlTowerRoleArn"
      AccountVendingAccountCreationCustomResourceBackerFunctionName:
        default: AccountCreationCustomResourceBacker
      AccountCreationCustomResourceBackerRoleName:
        default: AccountCreationCustomResourceBackerRole
      AccountVendingAccountCreationSNSTopicArn:
        ssm:
          name: "/foundational/account-vending/AccountVendingAccountNotificationCreatedTopicArn"
      AccountVendingStateMachineName:
        default: account-vending-state-machine
      AccountVendingStateMachineRoleName:
        default: StateMachineRole
      AccountVendingInputValidatorFunctionName:
        default: InputValidator
      AccountVendingInputValidatorRoleName:
        default: InputValidatorRole
      AccountVendingOrganizationsAccountCreatorFunctionName:
        default: OrganizationsAccountCreator
      AccountVendingOrganizationsAccountCreatorRoleName:
        default: OrganizationsAccountCreatorRole
      AccountVendingOrganizationsAccountWaiterFunctionName:
        default: OrganizationsAccountWaiter
      AccountVendingOrganizationsAccountWaiterRoleName:
        default: OrganizationsAccountWaiterRole
      AccountVendingControlTowerAccountCreatorFunctionName:
        default: ControlTowerAccountCreator
      AccountVendingControlTowerAccountCreatorRoleName:
        default: ControlTowerAccountCreatorRole
      AccountVendingControlTowerAccountWaiterFunctionName:
        default: ControlTowerAccountWaiter
      AccountVendingControlTowerAccountWaiterRoleName:
        default: ControlTowerAccountWaiterRole
      AccountVendingSubscriptionWaiterFunctionName:
        default: SubscriptionWaiter
      AccountVendingSubscriptionWaiterRoleName:
        default: SubscriptionWaiterRole

    deploy_to:
      tags:
        - tag: 'role:sct'
          regions: default_region
    outputs:
      ssm:
        - param_name: "/foundational/account-vending/AccountVendingAccountCreationCustomResourceBackerArn"
          stack_output: AccountVendingAccountCreationCustomResourceBackerArn
```

We recommend you create a new file named ServiceCatalogPuppet/manifests/account-vending.yaml so the resources needed for
account vending are kept together.  Please note you will to verify the deploy_to statements in the snippet to make sure
you have matches for your Organization / Control Tower management account and your SCT account.  You may need to add 
tags to these accounts or you may wish to update the tags in the snippet.

Once you have added this file you can commit and push your ServiceCatalogPuppet repository changes.  When the solution
runs the needed stacks will be created and you are ready to create an account!

### Creating an account using AWS Control Tower
To create an account using AWS Control Tower you will need to provision the Service Catalog product named 
account-vending-account-with-aws-control-tower.  This product has parameters that you would expect for account creation
and it has a parameter named AccountVendingAccountCreationCustomResourceBackerArn.  If you followed the instructions 
above the value of parameter will be in AWS Systems Manager in the parameter store as a parameter with the name
/foundational/account-vending/AccountVendingAccountCreationCustomResourceBackerArn.  When you provision the product the
account will be created.  If you provide account details for an already created account the solution will resume the 
account creation process.

### Creating an account using AWS Organizations
To create an account using AWS Organizations you will need to provision the Service Catalog product named 
account-vending-account-with-aws-organizations.  This product has parameters that you would expect for account creation
and it has a parameter named AccountVendingAccountCreationCustomResourceBackerArn.  If you followed the instructions 
above the value of parameter will be in AWS Systems Manager in the parameter store as a parameter with the name
/foundational/account-vending/AccountVendingAccountCreationCustomResourceBackerArn.  When you provision the product the
account will be created.  If you provide account details for an already created account the solution will resume the 
account creation process.