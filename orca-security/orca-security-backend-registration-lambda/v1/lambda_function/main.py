from aws_lambda_powertools.utilities.data_classes import event_source, SNSEvent
from aws_lambda_powertools import Logger
from crhelper import CfnResource
import requests
from orca import create_user_cloud_account
import json

logger = Logger(service="Cloudformation custom resource handler")
helper = CfnResource(
    json_logging=True, log_level="INFO", boto_level="CRITICAL", ssl_verify=None
)


@helper.create
def create(message, context):
    helper.Data["OrcaAccountId"] = create_user_cloud_account(
        message["ResourceProperties"].get("RoleArn"),
        message["ResourceProperties"].get("ExternalId"),
    )


@helper.update
def update(_, __):
    # TO-DO currently not in scope, External ID might change, role might change.
    # Basically , would be calling out delete account from orca, and creating new one.
    # However, deleting is also questionable.
    pass


@helper.delete
def delete(_, __):
    # TO-DO curently not in scope, AWS Account data must remain in Orca until Sec Team deletes data.
    pass


@event_source(data_class=SNSEvent)
@logger.inject_lambda_context(log_event=False)
def lambda_handler(event: SNSEvent, context):
    # Multiple records can be delivered in a single event
    for record in event.records:
        message = json.loads(record.sns.message)
        logger.info(message)
        helper(message, context)
