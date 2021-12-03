# scp-create

This cloudformation template uses custom resources backed by Lambda to create Service Control Policies (SCP).

## IMPORTANT - Portfolio Build Spec

Modify the Build Spec in the Factory portfolio.yaml to ensure the Python packages are installed - as specified by the requirements.txt 

For example:

```
  - Name: scp-create
    Owner: infrastructure-team@customer.com
    Description: Creates SCP
    Distributor: IT-Support-Customer
    SupportDescription: Contact us on Chime for help #central-it-team
    SupportEmail: infrastructure-team@customer.com
    SupportUrl: https://wiki.customer.com/infrastructure-team/self-service/
    Tags:
      - Key: lz-type
        Value: core
    Versions:
      - Name: v1
        Description: Creates SCP
        Active: True
        Source:
          Provider: CodeCommit
          Configuration:
            RepositoryName: scp-create
            BranchName: master
    BuildSpec: |
        version: 0.2
        phases:
          build:
            commands:
              - for dir in src/*; do pip install -r $dir/requirements.txt -t $dir/; done
            {% for region in ALL_REGIONS %}
              - aws cloudformation package --template $(pwd)/product.template.yaml --s3-bucket sc-factory-artifacts-${ACCOUNT_ID}-{{ region }} --s3-prefix ${STACK_NAME} --output-template-file product.template-{{ region }}.yaml
            {% endfor %}
        artifacts:
          files:
            - '*'
            - '**/*'

```

## Parameters

```
PolicyName:
Description: Name of SCP Policy
Type: String

PolicyDescription:
Description: Description of Policy
Type: String

S3Bucket:
Description: S3 bucket where policy has been uploaded
Type: String

S3Object:
Description: S3 object name of policy
Type: String

OrgRole:
Description: IAM Role Lambda uses to perform policy attach/delete actions.
Type: String
```

For example :
```
PolicyName = "deny_cloudtrail_stoplogging"
S3Bucket = "scp-policy-bucket"
S3Object = "deny_cloudtrail_stoplogging.json"
PolicyDescription = "Prevents Cloudtrail logging being turned off."
OrgRole = "arn:aws:iam::1234567890:role/OrgSCP"
```

## OrgRole

This IAM role requires the following permissions and would sit in the Organisation Master account:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "organizations:UpdatePolicy",
                "organizations:DetachPolicy",
                "organizations:AttachPolicy",
                "organizations:DeletePolicy",
                "organizations:DescribePolicy",
                "organizations:CreatePolicy",
                "organizations:ListPolicies"
            ],
            "Resource": "*"
        }
    ]
}
```

Typically this would be a cross account role with a trust relationship like:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::0987654321:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}
```

## Outputs
This product will output a PolicyId e.g. `p-dcvs56kz`. This Id will be used in the `SCP-Attach` product to attach the policy with a target.
