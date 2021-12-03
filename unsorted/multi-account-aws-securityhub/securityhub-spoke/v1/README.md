# securityhub-spoke

This well set up AWS Security Hub and assume an IAM role in the Security Account to perform self registration.

## Parameters

```
HubEnablerFunctionRole:
Type: String
Description: ARN of the SecurityHub role in the master that SecurityHubRegisterFunction will assume into

Email:
Type: String
Description: Email contact required for SecurityHub invite

HubAccountId:
Type: String
Description: The AccountId of the SecurityHub master account
```

