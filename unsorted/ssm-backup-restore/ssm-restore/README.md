# λ SSM-ParamStore-Restore

![Template Design] (SSM-Restore-Architecture.png)

### Description:
This serverless application creates a Lambda function which restores SSM parameters from an S3 backup. The function will restore from either the Main SSM bucket or the DR SSM bucket and once completed will send an email to the address specified during the backup process, in order to alert of its completion or communicate any errors. The function will also automatically terminate the Service Catalog product it belongs to which will delete the CloudFormation stack and the function itself, making it so that the user does not have to worry about 'cleaning up' after a restoration. Note that the function will also apply the bucket policy of the Main bucket to the DR bucket to facilitate the restoration.

### Returns:
This function is not made with a custom resource and therefore does not return a value to the CloudFormation stack that created it. The function is called based on a rate (every three minutes) in order to circumvent circular dependencies associated with the functionality and how custom resources work. The function sends a message to an SNS topic with its status which can be thought of as its 'return' and then terminates the Service Catalog product thus deleting the function. Therefore the function will run only once given that the restoration process takes less than three minutes. This rate can be adjusted - see the following example.

### Serverless Event Trigger Example:

```
  rRestoreParametersFunction:
    Type: AWS::Serverless::Function
    Properties:
      Events:
        AutoTrigger:
          Type: Schedule
          Properties:
            Schedule: "rate(5 minutes)"
```