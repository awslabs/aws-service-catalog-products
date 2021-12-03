## Cloud Custodian

Cloud Custodian is an open source stateless rules engine for policy definition and enforcement. The Cloud Custodian product for Service Catalog Tools consists of the following components:

- hub
- spoke
- codestar-connection


### Components

**Hub**

This product template creates all the resources needed for the custodian hub account.

**Spoke**

This product template creates all the resources needed within the custodian spoke account(s).

**Codestar-Connection**

This product template creates a Codestar Connection that is required if the repository provider type is anything other than CodeCommit. For example, if you are using Bitbucket or GitHub as your source repository provider, this product will need to be deployed into the custodian hub account in conjunction with the hub product.

- Note: Once the CodeStar Connection product has been deployed, the connection is in a PENDING status by default. You will need to make sure its status is in an AVAILABLE state by updating the connection in the console. Please refer to the latest version of the [CodeStar Connection product](https://github.com/awslabs/aws-service-catalog-products/tree/master/cloud-custodian/codestar-connection) README for the step by step process on how to complete this connection.
