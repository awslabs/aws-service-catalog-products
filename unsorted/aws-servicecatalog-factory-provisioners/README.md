# aws-servicecatalog-factory-provisioners
This is a solution to help deliver the IAM roles needed when provisioning Terraform products using 
aws-servicecatalog-factory and aws-servicecatalog-puppet

## Description
Deploys an IAM role that can be used by AWS CodePipeline to build out resources using Terraform

## Install Instructions

```bash
aws codecommit create-repository --repository-name aws-servicecatalog-factory-provisioners-terraform
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/aws-servicecatalog-factory-provisioners-terraform
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/aws-servicecatalog-factory-provisioners/terraform/v1 aws-servicecatalog-factory-provisioners-terraform --force
```

