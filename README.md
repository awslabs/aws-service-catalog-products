## AWS Service Catalog Products

This repository contains a number of solutions that can be easily deployed by the Service Catalog Tools 
([aws-service-catalog-factory](https://github.com/awslabs/aws-service-catalog-factory) and
[aws-service-catalog-puppet](https://github.com/awslabs/aws-service-catalog-puppet)).  The solutions are grouped by 
functional area:

- foundational - these are the solutions we recommend you use when building a foundation in AWS
- operations - these are the solutions we recommend to help you with operations
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

To import a solution you should copy each of the YAML files from its stacks, apps, workspaces and portfolios directories 
into the matching directory in your ServiceCatalogFactory repo.  If you are not going to be using AWS CodeCommit for the
source directory you will need to change that configuration.  Once you are ready commit the changes and run the factory
pipeline.  The new pipelines will be created and you are now ready to copy over the source code for the different parts.

### Deploying a solution

To deploy a solution you should copy the contents of the example-manifest.yaml into your ServiceCatalogPuppet repo into 
the path manifests/<functional_area>.yaml.  If there is a file in that path already you should merge the contents.  
Ensure you are happy with the parameters specified and the tags used before committing and pushing the change. 

### Contributing

If you have a solution you would like to contribute please 
[raise an issue](https://github.com/awslabs/aws-service-catalog-products/issues/new) to see verify if a similar solution
existing already or is in active development.  

Once you are ready to get started please fork the repository and complete the following TODOs:

1. choose which or create a new functional area your solution should be added to (see above for descriptions)
2. choose a unique and descriptive name - eg amazon-guardduty-multi-account
3. create a foundational/amazon-guardduty-multi-account/README.md
4. read over the programming standards section below
5. build out your solution in the directories foundational/amazon-guardduty-multi-account/stacks, foundational/amazon-guardduty-multi-account/apps, foundational/amazon-guardduty-multi-account/workspaces, foundational/amazon-guardduty-multi-account/portfolios
6. create each factory YAML file in each directory - eg. foundational/amazon-guardduty-multi-account/stacks/amazon-guardduty-multi-account.yaml 
7. create an foundational/amazon-guardduty-multi-account/example-manifest.yaml file containing each part of the solution and each of the parameters you have created for each part. 
8. raise a PR


## Programming Standards
Please read the following standards and follow them when implementing solutions for this repo

### General and Structure
1. You should not make changes to previously shared parts of your solution - you should create a new version of that part.
2. For each part of your solution that will be provisioned by the Service Catalog Tools you should use stacks, apps or workspaces - portfolios should be reserved for self service use cases.
3. When building your solution you should favour mono repos over poly repos - with the exception of when you are using portfolios.
4. When building solutions where parts need to be provisioned into different accounts try to limit the number of parts needed for each account to 1. This will reduce the complexity for users wishing to deploy your solution.
5. Each solution should be configured to use AWS CodeCommit as a git source to ensure a consistent experience when users import.

### Common parameters and tags
When writing your solution ensure you are using the autogenerated / provided parameters:

- SCTAccountId - puppet and factory account id
- SCTManifestAccounts - JSON encoded list of all accounts included in the manifest (including accounts in OUs specified) comprising of account_id and email attributes
- SCTManifestSpokes - same as SCTManifestAccounts but without including the SCT account. 
- SCTConfigRegions - JSON encoded list of regions specified in the config

You should also use the following tags in your example-manifest.yaml:

- role:sct - the account containing the Service Catalog Tools
- role:org_management - the AWS Organizations management account
- role:securitytooling - the account designated for security tooling 
- role:spoke - spoke accounts  

### AWS CloudFormation
1. All AWS CloudFormation parameter names should be prefixed with the solution name to avoid parameter clashes.
2. All AWS CloudFormation templates should pass a CFN Nag check
3. Each AWS CloudFormation template should have a description
4. Each AWS CloudFormation template parameter should have a description
5. Each AWS CloudFormation template output should have a description

### AWS IAM Resources
1. When creating IAM resources you should allow others to configure the path and role name via parameters.  
2. There should be default values for IAM path and role name values
3. IAM path default values should be the same value across all parts of the solution and should contain the solution category and an indication of the solution name in it.
4. IAM roles should follow least privilege or users should be able to specify an IAM boundary. 

### AWS Lambda
1. AWS Lambda function dependencies should be pinned to specific versions.
2. AWS Lambda functions should allow the configuration of log level via an environmental variable.

## Where is the old content
The previous master branch is still available as the branch archive

## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.


