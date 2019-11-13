# Put Metrics Product

This CloudFormation template creates custom Lambda functions and CloudWatch event rules for uploading the metrics for SC tools pipelines into CloudWatch.

**NOTE** : **This is for illustration purposes only and not approved for production use**.

## Parameters

```
IsDebugEnabled:
    Description: Set true/false to enable/ disable logging of the get metrics lambda
    Type: String
```

## Custom resources

- [PutMetrics Lambda Function](src/handler.py) : The lambda function will upload custom metrics into cloud watch for the pipeline execution status of `servicecatalog-factory-pipeline` and `servicecatalog-puppet-pipeline`. The states tracked are `SUCCEEDED`, `FAILED` and `CANCELED`. The metrics will be used to plot the CloudWatch dashboard for the pipelines

## Example

```
IsDebugEnabled = true
```
