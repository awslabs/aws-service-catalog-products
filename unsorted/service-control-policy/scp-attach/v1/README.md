# scp-attach

This cloudformation template uses custom resources backed by Lambda to attach Service Control Policies (SCP).

## IMPORTANT - Portfolio Build Spec

Modify the Build Spec in the Factory portfolio.yaml to ensure the Python packages are installed - as specified by the requirements.txt 

For example:

```
  - Name: scp-attach
    Owner: infrastructure-team@customer.com
    Description: Attaches SCP
    Distributor: IT-Support-Customer
    SupportDescription: Contact us on Chime for help #central-it-team
    SupportEmail: infrastructure-team@customer.com
    SupportUrl: https://wiki.customer.com/infrastructure-team/self-service/
    Tags:
      - Key: lz-type
        Value: core
    Versions:
      - Name: v1
        Description: Attaches SCP
        Active: True
        Source:
          Provider: CodeCommit
          Configuration:
            RepositoryName: scp-attach
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
PolicyId:
Description: The unique identifier (ID) of the policy that you want to attach to the target
Type: String

TargetId:
Description: The unique identifier (ID) of the root, OU, or account that you want to attach the policy to.
Type: String

OrgRole:
Description: IAM Role Lambda uses to perform policy attach/delete actions
Type: String
```

For example :
```
PolicyId = "p-dcvs56kz"
TargetId = "ou-aqba-fqufiols"
OrgRole = "arn:aws:iam::1234567890:role/OrgSCP"
```

### OrgRole

This IAM role requires the following permissions and would sit in the Organisation Master account:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "organizations:DetachPolicy",
                "organizations:AttachPolicy"
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