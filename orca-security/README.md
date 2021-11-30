# Orca Security

https://orca.security/, context aware Cloud Security.

## Watch Orca Security demo

https://orca.security/demo/

# Description
What this Stack does packages your Lambda code into Docker Image as custom build step in your Factory Account, which you can then deploy also in Factory account, and exponse via SNS to your AWS Organization. 

# Word of advice

Although this product is realword solution for Automating process of AWS Account Onboarding to Orca, main point here is to give an example of Custom build stage for packaging Docker Image and reusing in Lambda function. 
Starting hypothesis is that We have an AWS Organization with Factory/Puppet setup, and you have Subscription for Orca Security / API keys.
Once orca-security-backend-registration-lambda stack has been created, in AWS Console, you should go to Secrets manager service, put API Key used for generation of Session / Bearer tokens.
Secret name will be name of your Stack, eg orca-security-backend-registration-lambda.

orca-security-scanner-role product, should be deployed to all AWS accounts that you want registered with Orca Security, and this can be done as Custom Resource via SNS that is shared with ORG.
```yaml
RegisterAccountToOrca:
  Type: 'AWS::CloudFormation::CustomResource'
  Properties:
    ServiceToken: !Ref OrcaCustomResourceSNSTopicArn
    RoleArn: !GetAtt OrcaSecurityRole.Arn
    ExternalId: !Ref ExternalId
```

# Install Instructions

```bash
aws codecommit create-repository --repository-name orca-security-backend-registration-lambda
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/orca-security-backend-registration-lambda
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/orca-security/orca-security-backend-registration-lambda/v1 orca-security-backend-registration-lambda --force

aws codecommit create-repository --repository-name orca-security-scanner-role
git clone --config 'credential.helper=!aws codecommit credential-helper $@' --config 'credential.UseHttpPath=true' https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/orca-security-scanner-role
svn export https://github.com/awslabs/aws-service-catalog-products/trunk/orca-security/orca-security-scanner-role/v1 orca-security-scanner-role --force
```
