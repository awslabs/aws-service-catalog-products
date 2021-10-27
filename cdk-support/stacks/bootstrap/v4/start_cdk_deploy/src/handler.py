import boto3
import logging
from crhelper import CfnResource

logger = logging.getLogger(__name__)
helper = CfnResource(polling_interval=1)

try:
    pass
except Exception as e:
    helper.init_failure(e)


def start_build(project_name, environment_variables_override):
    codebuild = boto3.client("codebuild")
    bootstrapper_build = codebuild.start_build(
        projectName=project_name,
        environmentVariablesOverride=environment_variables_override,
    ).get("build")
    return bootstrapper_build.get("id")


def get_details_needed_for_build(event):
    request_type = event["RequestType"]
    properties = event.get("ResourceProperties")

    if request_type in ["Create", "Update"]:
        project_name = properties.get("CreateUpdateProject")
    else:
        project_name = properties.get("DeleteProject")

    args = [
        "CDK_DEPLOY_EXTRA_ARGS",
        "CDK_TOOLKIT_STACK_NAME",
        "PUPPET_ACCOUNT_ID",
        "CDK_DEPLOY_PARAMETER_ARGS",
        "CDK_DEPLOY_REQUIRE_APPROVAL",
        "NAME",
        "VERSION",
    ]
    environment_variables_override = [
        {"name": p, "type": "PLAINTEXT", "value": properties.get(p)}
        for p in args
    ]

    return project_name, environment_variables_override


def get_build_status_for(codebuild_build_id):
    client = boto3.client('codebuild')
    response = client.batch_get_builds(
        ids=[codebuild_build_id]
    )
    return response['builds'][0]['buildStatus']


@helper.create
@helper.update
@helper.delete
def create(event, context):
    logger.info(f'{event["RequestType"]}...')
    project_name, environment_variables_override = get_details_needed_for_build(event)
    logger.info(f'project_name is: {project_name}')
    logger.info(f'environment_variables_override is: {environment_variables_override}')
    codebuild_build_id = start_build(project_name, environment_variables_override)
    helper.Data['BuildId'] = codebuild_build_id


@helper.poll_create
@helper.poll_update
@helper.poll_delete
def poll_create(event, context):
    logger.info(f'Polling for {event["RequestType"]}...')
    codebuild_build_id = helper.Data['BuildId']

    status = get_build_status_for(codebuild_build_id)
    if status == "SUCCEEDED":
        return True
    elif status == "IN_PROGRESS":
        return None
    else:
        raise Exception(f"Codebuild Job: {codebuild_build_id} has status: {status}")


def handler(event, context):
    helper(event, context)
