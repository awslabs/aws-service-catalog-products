# product.template
# Description
Resources needed for custodian hub account
{"framework": "servicecatalog-products", "role": "product", "product-set": "cloud-custodian", "product": "pipeline", "version": "v1"}


## Parameters
The list of parameters for this template:

### C7NVersion 
Type: String 
Default: 0.9.6 
Description: which version of cloud custodian should be used 
### C7NMailerVersion 
Type: String 
Default: 0.6.5 
Description: which version of cloud custodian mailer should be used 
### C7NOrgVersion 
Type: String 
Default: 0.3.1 
Description: which version of cloud custodian c7n orgs should be used 
### CloudCustodianHubIAMRolePath 
Type: String 
Default: /cloudcustodian/ 
Description: Path to use for all IAM roles created in this template 
### CloudCustodianHubIAMRoleName 
Type: String 
Default: CustodianHub  
### CloudCustodianSQSMailerQueueName 
Type: String 
Default: CustodianSQSMailer 
Description: Provide a name for the Custodian SQS Queue 
### CloudCustodianSNSTopicDisplayName 
Type: String 
Default: CustodianAlerts 
Description: Enter a descriptive name for the SNS Alerts Topic 
### CloudCustodianSNSTopicName 
Type: String 
Default: CustodianAlerts 
Description: Enter a Topic Name for the SNS Alert Topic 
### RepositoryProviderType 
Type: String 
Default: CodeCommit 
Description: The name of your code repository provider 
### CloudCustodianPoliciesCodeCommitRepoName 
Type: String 
Default: CloudCustodianPolicies 
Description: Name to give the codecommit repo to use for the custodian policies 
### CodeStarConnectionArn 
Type: String  
Description: The ARN of the CodeStar Connection needed for third party repo integration 
### ProviderRepositoryId 
Type: String 
Default: (Ex: user/repository-name) 
Description: The owner and name of the repository where source changes are to be detected 
### ProviderRepositoryBranchName 
Type: String 
Default: master 
Description: The name of the branch where source changes are to be detected. 
### Regions 
Type: String 
Default: --region us-east-1  

## Resources
The list of resources this template creates:

### CloudCustodianSQSMailer 
Type: AWS::SQS::Queue 
Description: SQS Queue to be used by c7n 
### CloudCustodianSNSTopic 
Type: AWS::SNS::Topic 
Description: SNS Topic to be used by c7n 
### CloudCustodianAdminRole 
Type: AWS::IAM::Role 
Description: IAM Role to be used by c7n to run in the hub account 
### CloudCustodianCodeBuildRole 
Type: AWS::IAM::Role 
Description: IAM Role for codebuild to use when provisioning and cleaning up c7n policies 
### CloudCustodianDeploymentPipelineRole 
Type: AWS::IAM::Role 
Description: IAM Role to be used by the pipeline to orchestrate the provisioning and clean up of c7n policies 
### CloudCustodianDeploymentPipelineCustomPolicy 
Type: AWS::IAM::ManagedPolicy  
### CloudCustodianPoliciesRepo 
Type: AWS::CodeCommit::Repository 
Description: git repo for the policies 
### CloudCustodianPipelineArtifactStore 
Type: AWS::S3::Bucket 
Description: Bucket for artifacts from the pipeline 
### CloudCustodianPipeline 
Type: AWS::CodePipeline::Pipeline 
Description: Pipeline used to provision and clean up c7n policies 
### CloudCustodianPolicyValidationProject 
Type: AWS::CodeBuild::Project 
Description: Will validate policies in c7n-policies 
### CloudCustodianPolicyCleanupDryRunProject 
Type: AWS::CodeBuild::Project 
Description: Will run mugc dry-run policies for archive-policies 
### CloudCustodianPolicyCleanupProject 
Type: AWS::CodeBuild::Project 
Description: If you have a c7n-policies directory this will run mugc using them 
### CloudCustodianPolicyDeploymentDryRunProject 
Type: AWS::CodeBuild::Project 
Description: If you have a c7n-policies directory this will dry-run them, if you have c7n-org-policies directory it will dry-run them 
### CloudCustodianPolicyDeploymentProject 
Type: AWS::CodeBuild::Project 
Description: If you have a c7n-policies directory this will run them, if you have c7n-org-policies directory it will run them 
### CloudCustodianPolicyDeploymentOrgProject 
Type: AWS::CodeBuild::Project 
Description: if you have a c7n-org-policies directory this will run c7-org for you 

## Outputs
The list of outputs this template exposes:

### CloudCustodianSNSTopicArn 
Description: ARN of the Alerts SNS Topic  

### CloudCustodianSNSTopicName 
Description: Topic Name of the Alerts SNS Topic  

### CloudCustodianSQSMailerUrl 
Description: URL of the SQS queue  

### CloudCustodianSQSMailerUrlArn 
Description: Arn of the SQS queue  

### CloudCustodianSQSMailerUrlQueueName 
Description: QueueName of the SQS queue  

