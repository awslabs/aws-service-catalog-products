# SSM-ParamStore-Backup

![Template Design] (SSM-Store-Architecture.png)

### Description:
This service catalog product will create a primary S3 bucket in the same region with a bucket policy, and a Disaster Recovery (DR) bucket in the specified region. CloudFormation invokes Lambda as a Custom Resource to back-up SSM parameter store in the launched region to the primary S3 bucket.
The primary bucket will replicate to the DR bucket. After CREATE_COMPLETE for the CloudFormation Stack, a CloudWatch Rule is scheduled to invoke the backup lambda function based on the rate (Specified as a parameter). An SNS topic is created to notify the user when backups occur. 

### Returns:
1. SUCCESSFUL-200 CFN
 OR 
2. FAILURE - CFN Error and/or Lambda Error, CloudWatch Log Group

### λ CFN Custom Resource Examples:
```
  rBackupParameters:
    Type: Custom::CustomResource
    Properties:
      ServiceToken: !GetAtt rStoreParametersFunction.Arn
      
  rCreateDrBucket:
    Type: Custom::CustomResource
    Properties:
      ServiceToken: !GetAtt rCreateDrBucketFunction.Arn
      AccountID: !Sub '${AWS::AccountId}'
```
