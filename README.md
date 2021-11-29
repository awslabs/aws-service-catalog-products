## AWS Service Catalog Products

This repository contains a number of solutions that can be easily deployed by the Service Catalog Tools 
([aws-service-catalog-factory](https://github.com/awslabs/aws-service-catalog-factory) and
[aws-service-catalog-puppet](https://github.com/awslabs/aws-service-catalog-puppet)).  The solutions are grouped by 
functional area:

- foundational - these are the solutions we recommend you use when building a foundation in AWS
- reference - these are sample templates useful when you are learning how to write AWS Cloudformation templates
- unsorted - these are solutions that have been tested but not yet classified or standardised

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
drwxr-xr-x  6 user  group   192 19 Nov 14:07 stacks
drwxr-xr-x  6 user  group   192 19 Nov 14:07 portfolios
drwxr-xr-x  6 user  group   192 19 Nov 14:07 apps
drwxr-xr-x  6 user  group   192 19 Nov 14:07 workspaces
-rw-r--r--  1 user  group  2602 19 Nov 14:39 example-manifest.yaml
```

- The README.md explains what the solution does.
- The stacks directory is the source code for the parts of the solution that should be created as stacks
- The portfolios directory is the source code for the parts of the solution that should be created as products
- The apps directory is the source code for the parts of the solution that should be created as CDK apps
- The workspaces directory is the source code for the parts of the solution that should be created as Terraform workspaces
- The example-manifest.yaml is a valid YAML file providing an example of how to deploy the solution

Within each of the directorys stacks, portfolios, apps, workspaces you will find a file named 
amazon-guardduty-multi-account.yaml.  Each of the amazon-guardduty-multi-account.yaml files is a valid factory YAML file
that can be used to configure your install to build the parts of the solution that are needed.




### Importing a solution


### Deploying a solution


### Contributing

If you have a solution you would like to contribute please 
[raise an issue](https://github.com/awslabs/aws-service-catalog-products/issues/new) to see verify if a similar solution
existing already or is in active development.  

Once you are ready to get started please fork the repository and complete the following TODOs:

1. choose which functional area your solution should be added to
2. choose a unique and descriptive name - eg amazon-guardduty-multi-account
3. build out your solution in the directories amazon-guardduty-multi-account/stacks, amazon-guardduty-multi-account/apps, amazon-guardduty-multi-account/workspaces, amazon-guardduty-multi-account/portfolios
4. create the factory YAML files in 
5. create a directory for your solution and create 
  

## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.


