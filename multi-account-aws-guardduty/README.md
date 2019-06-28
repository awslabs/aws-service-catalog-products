# multi-account-aws-guardduty

## Description
With GuardDuty, you now have an intelligent and cost-effective option for continuous threat detection in the AWS Cloud. The service uses machine learning, anomaly detection, and integrated threat intelligence to identify and prioritize potential threats. GuardDuty analyzes tens of billions of events across multiple AWS data sources, such as AWS CloudTrail, Amazon VPC Flow Logs, and DNS logs.

**Contains 3 GuardDuty Products:**
- **GuardDuty Master** - To be run in the GuardDuty master Account - i.e. The Security Account. This creates a Role which ALL Spoke Accounts in the Org can assume to trigger an Invitation.
- **OrgMaster Bootstrap - To be run in the AWS Organization Master. This creates a role which can be assumed by ALL Spoke Accounts to describe accounts to get the email address of the spoke
- **GuardDuty Spoke** - To be run in every Spoke. it runs a Lambda Function to gather information about itself (the email address) and assume into Security Account to initiate the Invitation and create the detector

## Install Instructions
1. Deploy multi-account-aws-guardduty/guardduty-org-bootstrap into your org master account
2. Deploy multi-account-aws-guardduty/guardduty-master into your master account
3. Deploy multi-account-aws-guardduty/guardduty-spoke into your each spoke

```bash
aws codecommit create-repository --repository-name multi-account-aws-guardduty-guardduty-master
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/multi-account-aws-guardduty-guardduty-master
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/multi-account-aws-guardduty/guardduty-master/v1 multi-account-aws-guardduty-guardduty-master --force

aws codecommit create-repository --repository-name multi-account-aws-guardduty-guardduty-org-bootstrap
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/multi-account-aws-guardduty-guardduty-org-bootstrap
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/multi-account-aws-guardduty/guardduty-org-bootstrap/v1 multi-account-aws-guardduty-guardduty-org-bootstrap --force

aws codecommit create-repository --repository-name multi-account-aws-guardduty-guardduty-spoke
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/multi-account-aws-guardduty-guardduty-spoke
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/multi-account-aws-guardduty/guardduty-spoke/v1 multi-account-aws-guardduty-guardduty-spoke --force
```
