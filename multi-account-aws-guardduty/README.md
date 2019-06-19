# multi-account-guard-duty

## Architecture
DIAGRAM TBD

## Description
With GuardDuty, you now have an intelligent and cost-effective option for continuous threat detection in the AWS Cloud. The service uses machine learning, anomaly detection, and integrated threat intelligence to identify and prioritize potential threats. GuardDuty analyzes tens of billions of events across multiple AWS data sources, such as AWS CloudTrail, Amazon VPC Flow Logs, and DNS logs.

**Contains 3 GuardDuty Products:**
- **GuardDuty Master** - To be run in the GuardDuty master Account - i.e. The Security Account. This creates a Role which ALL Spoke Accounts in the Org can assume to trigger an Invitation.
- **OrgMaster Bootstrap - To be run in the AWS Organization Master. This creates a role which can be assumed by ALL Spoke Accounts to describe accounts to get the email address of the spoke
- **GuardDuty Spoke** - To be run in every Spoke. it runs a Lambda Function to gather information about itself (the email address) and assume into Security Account to initiate the Invitation and create the detector

## Install Instructions
1. Deploy GD-MAster-Role.yaml in the Organization Master. Use the Arn of the Deployed Role and as the value for GuardDutyAssumableOrgRoleArn in Security-GuardDutySpoke/product.template.yaml

2. Initialize products into service catalog via the factory

3. Create or Append the puppet manifest

 - deploy the guard-duty-spoke to all accounts and all desired regions

 - deploy guard-duty-master to the hub account and only to a single region

4. Please Refer to the Docs for explicit instructions on building factory products and writing the manifest

  - https://aws-service-catalog-puppet.readthedocs.io/en/latest/puppet/designing_your_manifest.html#purpose-of-the-manifest-file

  - https://aws-service-catalog-factory.readthedocs.io/en/latest/
