## AWS Service Catalog Products

This repository contains a number of solutions that can be easily deployed by the Service Catalog Tools 
([aws-service-catalog-factory](https://github.com/awslabs/aws-service-catalog-factory) and
[aws-service-catalog-puppet](https://github.com/awslabs/aws-service-catalog-puppet)).  The solutions are grouped by 
functional area:

- foundational - these are the solutions we recommend you use when building a foundation in AWS
- reference - these are sample templates useful when you are learning how to write AWS Cloudformation templates
- unsorted - these are solutions that have been tested but not yet classified

## Getting started

Within the functional area directories you will see a list of solutions:

```bash
ls -la foundational

drwxr-xr-x   8 user  group   256 18 Nov 21:49 .
drwxr-xr-x  15 user  group   480 29 Nov 09:55 ..
drwxr-xr-x   7 user  group   224 19 Nov 14:39 amazon-guardduty-multi-account
drwxr-xr-x   6 user  group   192 19 Nov 14:44 aws-securityhub-multi-account
drwxr-xr-x   6 user  group   192 19 Nov 12:58 delete-default-networking
```

Each solution should be deployable independently and each solution should be deployable with all other solutions in this
repository without issue.  

Each solution has the same consistent folder structure:

```bash
ls -la foundational/amazon-guardduty-multi-account

drwxr-xr-x  7 user  group   224 19 Nov 14:39 .
drwxr-xr-x  8 user  group   256 18 Nov 21:49 ..
-rw-r--r--  1 user  group     0 18 Nov 21:43 README.md
-rw-r--r--  1 user  group  1467 19 Nov 14:11 amazon-guardduty-multi-account.yaml
drwxr-xr-x  6 user  group   192 19 Nov 14:07 stacks
-rw-r--r--  1 user  group  2602 19 Nov 14:39 example-manifest.yaml
```

- The README.md explains what the solution does.
- The amazon-guardduty-multi-account.yaml filename matches the directory name.  It is a valid factory YAML file.
- The stacks directory is the source code for the parts of the solution that should be created as stacks
- The portfolios directory is the source code for the parts of the solution that should be created as products
- The apps directory is the source code for the parts of the solution that should be created as CDK apps
- The workspaces directory is the source code for the parts of the solution that should be created as Terraform workspaces
- The example-manifest.yaml is a valid YAML file providing an example of how to deploy the solution

## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.


