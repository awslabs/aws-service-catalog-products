## AWS Service Catalog Products

This repository contains a number of CloudFormation templates which can be used independently or as Products with AWS 
Service Catalog including the Open Source Tools AWS Service Catalog Factory and AWS Service Catalog Puppet. The 
templates include a number of the foundational AWS Services you may choose to manage Account Compliance including 
AWS Config, AWS CloudTrail and GuardDuty

## Getting started

In the root of this repository there are a collection of product sets.  Each set comprises of multiple products that 
should be deployed to achieve a goal.  You can see how and where each product within the set should be provisioned by
looking through the yaml files in the root of the product set.  For example the following portfolios.yaml file shows you
how to set up factory for one of the sets:

```yaml

Schema: factory-2019-04-01
Portfolios:
  Components:
    - Name: account-vending-account-creation-shared
      Owner: central-it@customer.com
      Description: lambda to used to back custom resources that create an AWS account and move it to an ou
      Distributor: central-it-team
      SupportDescription: Contact us on Chime for help
      SupportEmail: central-it-team@customer.com
      SupportUrl: https://wiki.customer.com/central-it-team/self-service/account-iam
      Tags:
        - Key: product-set
          Value: account-vending
      Versions:
        - Name: v2
          Description: lambda to used to back custom resources that create an AWS account and move it to an ou
          Active: True
          Source:
            Provider: CodeCommit
            Configuration:
              RepositoryName: account-vending-account-creation-shared
              BranchName: v2
          BuildSpec: |
            version: 0.2
            phases:
              install:
                runtime-versions:
                  python: 3.x
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

    - Name: account-vending-account-bootstrap-shared
      Owner: central-it@customer.com
      Description: Lambda and codebuild project needed to run servicecatalog-puppet bootstrap-spoke-as
      Distributor: central-it-team
      SupportDescription: Contact us on Chime for help
      SupportEmail: central-it-team@customer.com
      SupportUrl: https://wiki.customer.com/central-it-team/self-service/account-iam
      Tags:
        - Key: product-set
          Value: account-vending
      Versions:
        - Name: v2
          Description: Lambda and codebuild project needed to run servicecatalog-puppet bootstrap-spoke-as
          Active: True
          Source:
            Provider: CodeCommit
            Configuration:
              RepositoryName: account-vending-account-bootstrap-shared
              BranchName: v2
          BuildSpec: |
            version: 0.2
            phases:
              install:
                runtime-versions:
                  python: 3.x
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

    - Name: account-vending-account-creation
      Owner: central-it@customer.com
      Description: template used to interact with custom resources in the shared projects
      Distributor: central-it-team
      SupportDescription: Contact us on Chime for help
      SupportEmail: central-it-team@customer.com
      SupportUrl: https://wiki.customer.com/central-it-team/self-service/account-iam
      Tags:
        - Key: product-set
          Value: account-vending
      Versions:
        - Name: v1
          Description: template used to interact with custom resources in the shared projects.
          Active: True
          Source:
            Provider: CodeCommit
            Configuration:
              RepositoryName: account-vending-account-creation
              BranchName: master
```

And the manifest file shows how to set up puppet for one of the sets:

```yaml

schema: puppet-2019-04-01

launches:
  account-vending-account-creation-shared:
    portfolio: demo-central-it-team-portfolio
    product: account-vending-account-creation-shared
    version: v3
    parameters:
      AssumableRoleInRootAccountArn:
        default: arn:aws:iam::0123456789010:role/servicecatalog-puppet/AssumableRoleInRootAccount
      OrganizationAccountAccessRole:
        default: OrganizationAccountAccessRole
    outputs:
      ssm:
        - param_name: /account-vending/account-custom-resource-arn
          stack_output: AccountCustomResourceArn
    deploy_to:
      tags:
        - tag: scope:puppet-hub
          regions: default_region

  account-vending-account-bootstrap-shared:
    portfolio: demo-central-it-team-portfolio
    product: account-vending-account-bootstrap-shared
    version: v2
    parameters:
      AssumableRoleInRootAccountArn:
        default: arn:aws:iam::0123456789010:role/servicecatalog-puppet/AssumableRoleInRootAccount
    outputs:
      ssm:
        - param_name: /account-vending/bootstrapper-project-custom-resource-arn
          stack_output: BootstrapperProjectCustomResourceArn
    deploy_to:
      tags:
        - tag: scope:puppet-hub
          regions: default_region

  account-vending-account-001:
    portfolio: demo-central-it-team-portfolio
    product: account-vending-account-creation
    version: v2
    depends_on:
      - account-vending-account-creation-shared
      - account-vending-account-bootstrap-shared
    parameters:
      Email:
        default: "mailing-list+account-001@somewhere.com"
      AccountName:
        default: "account-001"
      OrganizationAccountAccessRole:
        default: "OrganizationAccountAccessRole"
      IamUserAccessToBilling:
        default: "ALLOW"
      TargetOU:
        default: /
      AccountVendingCreationLambdaArn:
        ssm:
          name: /account-vending/account-custom-resource-arn
      AccountVendingBootstrapperLambdaArn:
        ssm:
          name: /account-vending/bootstrapper-project-custom-resource-arn
    deploy_to:
      tags:
        - tag: scope:puppet-hub
          regions: default_region
```

Within the manifest.yaml file you should be able to use the values of the tags on the launches/stacks to understand
which account the solution should be provisioned into.

## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.


