# Get Metrics Product

This CloudFormation template creates custom Lambda functions and CloudWatch event rules for uploading the JSON output from SC tools into the S3 bucket hosting the static website.

**NOTE** : **This is for illustration purposes only and not approved for production use**.

## Parameters

The manifest.yaml should use the SSM to provide `S3BucketNameForStaticWebsite` value from the [static-web-app product](../../static-web-app/v1/README.md)
```
S3BucketNameForStaticWebsite:
    Description: S3 bucket name for hosting the static website
    Type: String
IsDebugEnabled:
    Description: Set true/false to enable/ disable logging of the get metrics lambda
    Type: String
```

## Custom resources

- [GetMetrics Lambda Function](src/handler.py) : The lambda function will use the service catalog commands to generate a `list-launches.json` and `show-pipelines.json`. The JSON files are uploaded into the S3 bucket at runtime. The JSON files are uploaded everytime we have an execution of the `servicecatalog-factory-pipeline` and `servicecatalog-puppet-pipeline`

## Example

```
S3BucketNameForStaticWebsite = static-s3-website
IsDebugEnabled               = true
```

