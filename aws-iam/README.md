# aws-iam

## Architecture
DIAGRAM TBD

## Description
Deploys a highly configurable IAM Group/Role strategy that allows users to assume roles into other accounts from the security account. Using IAM Groups ensures permissions are for users in those assumed roles are locked down.

## Install Instructions
1. Initialize products into service catalog via the factory

2. Create or Append the puppet manifest
 - Set iam-groups-security-account to an account specific deployment with the security account as the target.

 - deploy iam-assume-roles-spoke to all accounts

3. Please Refer to the Docs for explicit instructions on building factory products and writing the manifest

 - https://aws-service-catalog-puppet.readthedocs.io/en/latest/puppet/designing_your_manifest.html#purpose-of-the-manifest-file

 - https://aws-service-catalog-factory.readthedocs.io/en/latest/
