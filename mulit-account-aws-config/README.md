# multi-account-aws-config

## Architecture
DIAGRAM TBD

## Description
Enables AWS Config across all accounts this product is deployed into, Creates an aggregated SNS Topic within the security account which will forward config event messages to a designated email address.

Config is a service that enables you to assess, audit, and evaluate the configurations of your AWS resources. Config continuously monitors and records your AWS resource configurations and allows you to automate the evaluation of recorded configurations against desired configurations and determine your overall compliance against the configurations specified in your internal guidelines.

enabling you to simplify compliance auditing, security analysis, change management, and operational troubleshooting.  


## Install Instructions
1. Initialize products into service catalog via the factory

2. Create or Append the puppet manifest

 - deploy aws-config-enable and aws-config-rules to all accounts

 - deploy aws-config-sns-hub to the security account

 - deploy aws-config-sns-spoke to all spoke accounts

3. Please Refer to the Docs for explicit instructions on building factory products and writing the manifest

  - https://aws-service-catalog-puppet.readthedocs.io/en/latest/puppet/designing_your_manifest.html#purpose-of-the-manifest-file

  - https://aws-service-catalog-factory.readthedocs.io/en/latest/
