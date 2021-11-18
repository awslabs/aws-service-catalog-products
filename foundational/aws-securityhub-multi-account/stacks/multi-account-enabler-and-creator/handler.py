import logging
import boto3
import os
import json

boto_level = os.environ.get("BOTO_LOG_LEVEL", logging.CRITICAL)
logging.getLogger("boto").setLevel(boto_level)
logging.getLogger("boto3").setLevel(boto_level)
logging.getLogger("botocore").setLevel(boto_level)
logging.getLogger("urllib3").setLevel(boto_level)

log_level = os.environ.get("LOG_LEVEL", logging.WARNING)
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)s %(threadName)s %(message)s", level=logging.INFO
)
logger.setLevel(log_level)


def update_organization_configuration(client):
    describe_organization_configuration_response = client.describe_organization_configuration()
    if describe_organization_configuration_response.get("MemberAccountLimitReached", False) is True:
        raise Exception("Member account limit reached")
    if describe_organization_configuration_response.get("AutoEnable", False) is not True:
        logger.info("AutoEnabled was not enabled")
        client.update_organization_configuration(
            AutoEnable=True,
        )
        logger.info("AutoEnabled set to true")


def enable_organization_admin_account(client, admin_account_id):
    client.enable_organization_admin_account(
        AdminAccountId=admin_account_id
    )


def is_an_organization_admin_accounts(client, account_id):
    paginator = client.get_paginator('list_organization_admin_accounts')
    for page in paginator.paginate():
        for admin_accounts in page.get("AdminAccounts", []):
            if admin_accounts.get("AdminAccountId") == account_id:
                return admin_accounts.get("AdminStatus") == "ENABLED"
    return False


def make_an_organization_admin_accounts(client, account_id):
    client.enable_organization_admin_account(
        AdminAccountId=account_id
    )
    logger.info(f"made {account_id} an org admin account")


def get_org_client(region):
    security_hub_multi_account_delegate_admin_role_arn = os.environ.get(
        "SECURITY_HUB_MULTI_ACCOUNT_DELEGATE_ADMIN_ROLE_ARN")
    sts = boto3.client('sts')
    assumed_role_object = sts.assume_role(
        RoleArn=security_hub_multi_account_delegate_admin_role_arn,
        RoleSessionName='security_hub_multi_account_delegate_admin_role_arn',
    )
    credentials = assumed_role_object['Credentials']
    kwargs = {
        "aws_access_key_id": credentials['AccessKeyId'],
        "aws_secret_access_key": credentials['SecretAccessKey'],
        "aws_session_token": credentials['SessionToken'],
    }
    return boto3.client('securityhub', region_name=region, **kwargs)


def create_client(region):
    return boto3.client('securityhub', region_name=region)


def ensure_all_are_members(client, accounts_to_ensure):
    create_members_response = client.create_members(
        AccountDetails=[{
            'AccountId': account_to_ensure.get("account_id"),
            'Email': account_to_ensure.get("email")
        } for account_to_ensure in accounts_to_ensure]
    )
    if len(create_members_response.get("UnprocessedAccounts", [])) > 0:
        raise Exception(f"There were unprocessed accounts: {create_members_response.get('UnprocessedAccounts')}")
    logger.info(f"created members")


def handle(event, context):
    logger.info("starting")
    logger.debug(json.dumps(event, default=str))
    region = event.get("region")
    account_id = event.get("account_id")
    accounts_to_ensure = event.get("accounts_to_ensure", [])

    securityhub = create_client(region)

    org_client = get_org_client(region)
    if not is_an_organization_admin_accounts(org_client, account_id):
        logger.info(f"{account_id} is not an org admin account")
        make_an_organization_admin_accounts(org_client, account_id)

    update_organization_configuration(securityhub)
    ensure_all_are_members(securityhub, json.loads(accounts_to_ensure))
    logger.info("created")


if __name__ == "__main__":
    os.environ[
        'SECURITY_HUB_MULTI_ACCOUNT_DELEGATE_ADMIN_ROLE_ARN'] = 'arn:aws:iam::156551640785:role/foundational/SecurityHubMultiAccount/DelegateAdminRole'
    sample_parameters = dict(
        region="eu-west-1",
        account_id="338024302548",
        accounts_to_ensure=json.dumps([
            {"account_id": "156551640785", "email": "eamonnf+SCT-demo-hub@amazon.co.uk"},
            {"account_id": "029953558454", "email": "eamonnf+SCT-demo-spoke-5@amazon.co.uk"},
            {"account_id": "511601033246", "email": "eamonnf+SCT-demo-spoke-4@amazon.co.uk"},
            {"account_id": "574018543153", "email": "eamonnf+SCT-demo-spoke-3@amazon.co.uk"},
            {"account_id": "338024302548", "email": "eamonnf+SCT-demo-spoke-2@amazon.co.uk"},
        ])
    )

    sample_context = None
    handle(sample_parameters, sample_context)
