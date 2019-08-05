# Monitoring

This is a solution to monitor the service catalog factory and puppet pipelines using dashboards in CloudWatch and a static website hosted on S3

## Description

Deploys a service-catalog-tools-dashboard product which creates the dashboard for monitoring

## Install Instructions

```bash
aws codecommit create-repository --repository-name service-catalog-tools-dashboard
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/service-catalog-tools-dashboard
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/monitoring/service-catalog-tools-dashboard/v1 service-catalog-tools-dashboard --force
```

## Usage instructions

Copy the config from manifest.yaml. The launch of `service-catalog-tools-dashboard` should appear in your manifest only once. Refer the dashboard product [README](dashboard/README.md) for more details.
