# AWS-Config-Aggregator

This template creates an AWS Config Aggregator using AWS Organizations.


## Parameters

```
ConfigurationAggregatorName:
Type: String
Description: |
    "The name of the aggregator. Member must satisfy regular expression pattern: [\w\-]+"

AllAwsRegions:
Type: String
Default: true
AllowedValues: [true, false]
Description: |
    If true, aggregate existing AWS Config regions and future regions.

SpecificAwsRegions:
Type: CommaDelimitedList
Default: ""
Description: |
    Optional - If AllAwsRegions is true then this is not used. CommaDelimitedList of source regions being aggregated.

```

## Outputs

```
OrgConfigRole:
Description: Arn of IAM role used by AWS Config for Organization permissions
Value: !GetAtt OrgConfigAggregatorRole.Arn

OrgConfigName:
Description: Configuration Aggregator Name
Value: !Ref OrgConfigAggregatorAll
Condition: UseAllAwsRegions

OrgConfigName:
Description: Configuration Aggregator Name
Value: !Ref OrgConfigAggregatorSpecific
Condition: UseSpecificAwsRegions
```