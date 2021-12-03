# networking 

## Description
With this product set you can create a VPC and a public subnet



## Install Instructions

```bash
aws codecommit create-repository --repository-name networking-vpc
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/networking-vpc
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/networking/vpc/v1 networking-vpc --force

aws codecommit create-repository --repository-name networking-public-subnet
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/networking-public-subnet
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/networking/vpc/v1 networking-public-subnet --force
```
