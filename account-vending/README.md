# account-vending
This is a solution to help deliver an account vending machine.

## Description
This creates an AWS Account vending machine so your customers can create their own AWS Accounts using AWS Service Catalog.

There are three AWS Service Catalog Products in this solution.  ```account-bootstrap-shared``` and 
```account-creation-shared``` will provisioon lambdas 

## Install instructions

### Dependencies
In order to use the Account-vending machine you will need the ARN of an AWS IAM Role in your Organizations root account.

You can create that role using the template ```org-bootstrap.template.yaml```

Once you have provisioned that role keep a note of the ARN you will need it later.

### Bootstrapping
T

### Preparing the shared account creation product
You must add the ```account-creation-shared-product``` to your servicecatalog-factory portfolio:
```yaml
    Components:      
      - Name: account-vending-account-creation-shared
        Owner: central-it@customer.com
        Description: lambda to used to back custom resources that create an AWS account and move it to an ou
        Distributor: central-it-team
        SupportDescription: Contact us on Chime for help #central-it-team
        SupportEmail: central-it-team@customer.com
        SupportUrl: https://wiki.customer.com/central-it-team/self-service/account-iam
        Tags:
        - Key: product-type
          Value: iam
        Versions:
          - Name: v1
            Description: lambda to used to back custom resources that create an AWS account and move it to an ou
            Active: True
            Source:
              Provider: CodeCommit
              Configuration:
                RepositoryName: account-vending-account-creation-shared
                BranchName: master
            BuildSpec: |
              version: 0.2
              phases:
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
``` 

I have named my product ```account-vending-account-creation-shared``` and it is coming from the repo 
```account-vending-account-creation-shared```.

### Preparing the shared bootstrap account product
You must add the ```account-bootstrap-shared-product``` to your servicecatalog-factory portfolio:

```yaml
      - Name: account-vending-account-bootstrap-shared
        Owner: central-it@customer.com
        Description: Lambda and codebuild project needed to run servicecatalog-puppet bootstrap-spoke-as
        Distributor: central-it-team
        SupportDescription: Contact us on Chime for help #central-it-team
        SupportEmail: central-it-team@customer.com
        SupportUrl: https://wiki.customer.com/central-it-team/self-service/account-iam
        Tags:
        - Key: product-type
          Value: iam
        Versions:
          - Name: v1
            Description: Lambda and codebuild project needed to run servicecatalog-puppet bootstrap-spoke-as
            Active: True
            Source:
              Provider: CodeCommit
              Configuration:
                RepositoryName: account-vending-account-bootstrap-shared
                BranchName: master
            BuildSpec: |
              version: 0.2
              phases:
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
```

I have named my product ```account-vending-account-bootstrap-shared``` and it is coming from the repo 
```account-vending-account-bootstrap-shared```.

### Preparing the account creation product:
You must add the ```account-creation-product``` to your servicecatalog-factory portfolio:

```yaml
      - Name: account-vending-account-creation
        Owner: central-it@customer.com
        Description: template used to interact with custom resources in the shared projects
        Distributor: central-it-team
        SupportDescription: Contact us on Chime for help #central-it-team
        SupportEmail: central-it-team@customer.com
        SupportUrl: https://wiki.customer.com/central-it-team/self-service/account-iam
        Tags:
        - Key: product-type
          Value: iam
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

I have named my product ```account-vending-account-creation``` and it is coming from the repo 
```account-vending-account-creation```.

Once you have added the products to your portfolio, you must commit your portofolio and set up your product 
git repos and ensure those pipelines run correctly.

## Using the account vending machine
Log into the console and navigate to Service Catalog.  You should see a section named Provisioned products list.  
Within that section you will see a product with the name you specified - I chose ```account-vending-account-creation```

Click the product, select launch and enter your parameters, click next a few more times and you will have a bootstrapped 
account.
