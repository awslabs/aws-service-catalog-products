# service-control-policy
This is a solution that provides the ability to create & attach Service Control Policies.

## Description
Service control policies (SCPs) are one type of policy that you can use to manage your organization. SCPs offer central control over the maximum available permissions for all accounts in your organization, allowing you to ensure your accounts stay within your organization’s access control guidelines.
 
scp-create can be used to create a service control policy. scp-attach will then be used to attach this policy against an Organizational Unit or Account.

## Install Instructions

```bash
aws codecommit create-repository --repository-name scp-create
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/scp-create
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/service-control-policy/scp-create/v1 scp-create --force

aws codecommit create-repository --repository-name scp-attach
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/scp-attach
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/service-control-policy/scp-attach/v1 scp-attach --force
```
