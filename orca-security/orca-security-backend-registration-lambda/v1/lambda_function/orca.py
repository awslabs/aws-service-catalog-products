from utils import BearerAuthSecretsManager
from utils import CrossAccountClientContextManager
from aws_lambda_powertools import Logger
import requests

logger = Logger(service="Orca Backend Registration")


def create_user_cloud_account(
    customer_role_arn: str,
    customer_role_external_id: str,
) -> dict:
    with CrossAccountClientContextManager(
        "iam",
        customer_role_arn,
        "orca-onboarding-automation",
        external_id=customer_role_external_id,
    ) as client:
        account_alias = client.list_account_aliases()["AccountAliases"][0]
    account_id = customer_role_arn.split(":")[4]
    account_details = {
        "aws": {
            "aws_role_arn": customer_role_arn,
            "external_id": customer_role_external_id,
        }
    }
    account_data = {
        "name": "{} ({})".format(account_alias, account_id),
        "account_details": account_details,
        "skip_permission_check": True,
    }
    bt = BearerAuthSecretsManager()
    res = requests.post(
        bt.api_endpoint_url + "/cloudaccount", auth=bt, json=account_data
    )
    res.raise_for_status()
    res_json = res.json()
    logger.info(res_json)
    if "cloud_account_id" not in res_json.get("data", {}):
        raise Exception(f"rest api post api/cloudaccount failed!")
    cloud_account_id = res_json["data"]["cloud_account_id"]
    logger.info(f"Cloud Account {cloud_account_id} created.")
    return cloud_account_id
