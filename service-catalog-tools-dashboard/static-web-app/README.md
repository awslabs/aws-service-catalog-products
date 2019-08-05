# Service Catalog Tools Dashboard

This CloudFormation template creates monitoring dashboard product for tracking the status of the products provisioned using the service catalog factory and puppet tools

**NOTE** : **This is for illustration purposes only and not approved for production use**.

## Assumption

We expect the static website to be manually deployed into the S3 bucket created as part of the resources. The HTML, CSS and JS files for the static website are available in `/static-website/public_html` folder. This will be a one time deployment, unless there is requirement to change the user interface of the dashboard

## Parameters

```
CIDRForDashboardAccess:
    Description: IP CIDR range which will be allowed to access the monitoring dashboard hosted on S3
    Type: String
```

## Source code for static website

The source code for the static website is available in the `/web-dashboard`. Please refer the [README](v1/web-dashboard/README.md)

## Custom resources

- [GetMetrics Lambda Function](../get-metrics/v1/src/handler.py) : The lambda function will use the service catalog commands to generate a `list-launches.json` and `show-pipelines.json`. The JSON files are uploaded into the S3 bucket at runtime. The JSON files are uploaded everytime we have an execution of the `servicecatalog-factory-pipeline` and `servicecatalog-puppet-pipeline`
- [PutMetrics Lambda Function](../put-metrics/v1/src/handler.py) : The lambda function will upload custom metrics into cloud watch for the pipeline executon status of `servicecatalog-factory-pipeline` and `servicecatalog-puppet-pipeline`. The states tracked are `SUCCEEDED`, `FAILED` and `CANCELED`. The metrics will be used to plot the cloudwatch dashboard for the pipelines

## Example

```
CIDRForDashboardAccess = 192.168.0.0/20
```
