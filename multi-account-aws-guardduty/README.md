# multi-account-guard-duty

## Architecture
DIAGRAM TBD

## Description

deploys GuardDuty Master and spoke products, With GuardDuty, you now have an intelligent and cost-effective option for continuous threat detection in the AWS Cloud. The service uses machine learning, anomaly detection, and integrated threat intelligence to identify and prioritize potential threats. GuardDuty analyzes tens of billions of events across multiple AWS data sources, such as AWS CloudTrail, Amazon VPC Flow Logs, and DNS logs.

## Install Instructions
1. Deploy GD-MAster-Role.yaml in the Organization Master. Use the Arn of the Deployed Role and as the value for GuardDutyAssumableOrgRoleArn in Security-GuardDutySpoke/product.template.yaml

2. Initialize products into service catalog via the factory

3. Create or Append the puppet manifest

 - deploy the guard-duty-spoke to all accounts and all desired regions

 - deploy guard-duty-master to the hub account and only to a single region

4. Please Refer to the Docs for explicit instructions on building factory products and writing the manifest

  - https://aws-service-catalog-puppet.readthedocs.io/en/latest/puppet/designing_your_manifest.html#purpose-of-the-manifest-file

  - https://aws-service-catalog-factory.readthedocs.io/en/latest/
