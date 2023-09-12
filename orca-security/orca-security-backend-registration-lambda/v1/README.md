# Orca role template location

```plaintext
https://orca-staticfiles-production-eu-central-1.s3.amazonaws.com/production/cf_templates/default_policy.json
```

# Orca API

```plaintext
https://orcasecurity.zendesk.com/hc/en-us/articles/360039310532-Orca-REST-API-Reference
```

# AWS Secrets Manager

Provisioned Stack creates an Secret Manager secret, it is necessary to replace API_KEY with valid one.

```plaintext
{
	"API_KEY": "REPLACE_ME",
	"API_ENDPOINT_URL": "https://app.eu.orcasecurity.io/api"
}
```