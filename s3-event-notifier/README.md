# S3 Event Notifier

This solution creates an event driven approach to process S3 PUT events via SQS and Lambda.

![Template Design](s3-event-notifier-design.png)

## Description

* Deploys one product which will listen to any `PUT` events on S3 `files/` prefix folder
* Sends the event to a SQS queue
* Configures a dead-letter queue in case of failures
* Uses KMS encryption on the SQS queues
* Lambda trigger is configured on the SQS queue to extract the `bucketName`, `key` and `eventTime`

## Install Instructions

```bash
aws codecommit create-repository --repository-name s3-event-notifier
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.us-east-2.amazonaws.com/v1/repos/s3-event-notifier
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/s3-event-notifier/v1 s3-event-notifier --force
```

## Usage Instructions

- Copy the config from the portfolio.yaml. Here we are providing the details on the repository and BuildSpec needed for packaging the products
- Copy the config from manifest.yaml. We will be having one launch in the manifest
