# How it Works

The following describes the different steps of the process that are execute when provisioning new accounts using the `aws-service-catalog-account-creation` product.

## Steps

1. ### **Get the OU for the Commercial Account**
    The first step in the process is to get the OU identifier for the Commercial account based on the *Commercial Account Type* and *Commercial Account Group* that were provided. 
    
    This step is the `OUDetails` resource in the product template. `OUDetails` is a custom resource that calls the AWS Lambda function that is provisioned from the `account-type-to-organizational-unit-chooser` product. This Lambda function contains an object that maps a given account type, group and partition to an OU identifier. The OU identifier is then returned and is later accessed in the stack as `OUDetails.OrganizationalUnitName`.   

2. ### **Get the OU for the GovCloud Account**
    The second step in the process is to get the OU identifier for the GovCloud account based on the *GovCloud Account Type* and *GovCloud Account Group* that were provided. 
    
    This step is the `GovCloudOUDetails` resource in the product template. `GovCloudOUDetails` is the same as `OUDetails` with the only difference being that it passes different values for the account type, group and partition. The same Lambda function from the `account-type-to-organizational-unit-chooser` product is called. The OU identifier that is returned in this instance is later accessed in the stack as `GovCloudOUDetails.OrganizationalUnitName`.

3. ### **Create the Commercial and GovCloud Accounts**
    The next step in the process is to create the Commercial account and the linked GovCloud account using the *Account Email* and *Account Name* values that were provided.

    This step is the `Account` resource in the product template. `Account` is a custom resource that calls the AWS Lambda function that is provisioned from the `account-creation-shared` product. This Lambda function first checks to see if the account already exists. If it does, it will continue out of the function and proceed to the next step. If it does not, it will next check to see if you are creating a Commerical only account or a GovCloud account and then call the corresponding API to create the account(s).

    When creating GovCloud accounts, the following will occur:<br>
    1. A Commercial account is created within the Commericial organization
    2. A GovCloud account is created as a standalone account in the GovCloud partition. This account is linked to the Commerical account that was created above. A later step in the process will automate the onboarding of the GovCloud account which includes adding it to the Organization in GovCloud

4. ### **Move the Commercial Account to the OU**
    The next step is to move the newly created Commerical account to the correct OU in the Commercial Organization. This OU is the one that was returned from step 1 in the process.

    This step is the 'MoveToOU' resource in the product template. `MoveToOU` is a custom resource that calls the AWS Lambda function that is provisioned from the `move-to-ou` product. This Lambda function performs the following:<br>
    1. Assumes a role in the Organization root account
    2. Checks to make sure the account is in the organization
    3. If the OU identifier (`OUDetails.OrganizationalUnitName`) is using the path format, the function looks up the OU ID for the path
    4. Moves the account into the OU

5. ### **Wait for the Commercial Account to Become Available**
    Before the Commercial account can be bootstrapped for Service Catalog Puppet, the AWS CodeBuild and AWS CloudFormation services must be available in the account. This step waits until those services are available before proceeding to the next step.

    This step is the `AccountWaiter1` resource in the product template. `AccountWaiter1` is a custom resource that calls the AWS Lambda function that is provisioned from the `account-waiter` product. This Lambda function executes an AWS CodeBuild project which is also provisioned from the `account-waiter` product. This CodeBuild project will install `aws-service-catalog-puppet` and then run the `servicecatalog-puppet --info wait-for-code-build-in` command. This command will wait for CodeBuild and CloudFormation to be available in the account before returning and completing the build which also completes the step. 

6. ### **Send Notification that the Commercial Account was Created**
    Once the Commercial account is available, the next step is to send a notification that the account was created using SNS.

    This step is the `Notifier` resource in the product template. `Notifier` is a custom resource that calls the AWS Lambda function that is provisioned from the `account-create-update-notifier` product. This Lambda function builds a message with the account details of the new Commercial account and publishes the message to the SNS topic which is also provisioned by the `account-create-update-notifier` product. 

    You can setup your own subscriptions to the SNS topic so that the appropriate people are notified and/or events are triggered. If you have provisioned the `account-creation-notifier-cfh-handler` product with a custom HTTP POST endpoint as the `CFHAccountCreateUpdatePostUrl` parameter, that will create an AWS Lambda function that is subscribed to the SNS topic and will relay the messages to the HTTP POST endpoint. This is a requirement for the GovCloud account in the following step.

7. ### **Send Notification that the GovCloud Account was Created**
    The next step is to send a notification that the GovCloud account was created using SNS. This notification is important as it is used to trigger the onboarding process for the GovCloud account

    This step is the `GovCloudNotifier` resource in the product template. `GovCloudNotifier` is a custom resource that calls the AWS Lambda function that is provisioned from the `account-create-update-notifier` product. This can be the exact same Lambda function as the `Notifier` resource for the Commercial account notification or it can be another version of the `account-create-update-notifier` that you have provisioned.

    This will use the same SNS topic as the Commercial account. You can setup your own subscriptions to the SNS topic so that the appropriate people are notified and/or events are triggered. 
    
    The GovCloud account onboarding process requires the notification to trigger an AWS Lambda function in the GovCloud Organization master account. For this to work correctly, you must have completed the following steps:
    1. Provisioned the `govcloud-account-onboard` and `account-bootstrap-shared-org-bootstrap` products in the GovCloud Organization management account
    2. Provisioned the `govcloud-account-onboard-puppet-bootstrap` and `account-bootstrap-shared` products in your GovCloud Service Catalog Puppet account
    3. Provisioned the `account-creation-notifier-cfh-handler` product in the Commercial Organization management account with the `CFHAccountCreateUpdatePostUrl` parameter set to the API Gateway endpoint URL in the GovCloud Organization management account. This API Gateway endpoint is provisioned from the `govcloud-account-onboard` product and should look like this `https://{APIGWID}.execute-api.us-gov-west-1.amazonaws.com/Prod/onboard-account` 

    If those requirements are in place, the SNS notification will call the Lambda function from the `account-creation-notifier-cfh-handler` which will relay the message to the Lambda function in the GovCloud Organization management account. That Lambda function will then complete the following:
    1. Invite the new GovCloud account to the GovCloud Organization
    2. Assume a role in the new GovCloud account and accept the invitation to join the GovCloud Organization
    3. Move the new GovCloud account to the correct OU (`GovCloudOUDetails.OrganizationalUnitName`) in the GovCloud Organization
    4. Assume a role in the GovCloud Service Catalog Puppet account
    5. Bootstrap the new GovCloud account as a spoke of the GovCloud Service Catalog puppet account

8. ### **Bootstrap the Commercial Account**
    The last step in the process is to bootstrap the new Commerical account for Service Catalog Puppet.

    This step is the `Bootstrap` resource in the product template. `Bootstrap` is a custom resource that calls the AWS Lambda function that is provisioned from the `account-bootstrap-shared` product. This Lambda function executes an AWS CodeBuild project which runs the `servicecatalog-puppet bootstrap-spoke-as` command to complete the bootstrap process.

9. ### **Output the Account IDs**
    Once this process has completed, the AWS CloudFormation stack will provide the *Commerical Account ID* and *GovCloud Account ID* as output values.