# Static Web App Product

This CloudFormation template creates dashboard product hosted on S3 bucket for tracking the status of the SC tools.

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

The source code for the static website is available in the `/web-dashboard`. Please refer the [README](web-dashboard/README.md)

## Example

```
CIDRForDashboardAccess = 192.168.0.0/20
```
