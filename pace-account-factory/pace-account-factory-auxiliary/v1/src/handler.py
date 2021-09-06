import os

from crhelper import CfnResource
import logging
from betterboto import client as betterboto_client

logger = logging.getLogger(__name__)

helper = CfnResource(
    json_logging=False,
    log_level='DEBUG',
    boto_level='CRITICAL',
    sleep_on_delete=120,
    ssl_verify=None
)

try:
    ## Init code goes here
    pass
except Exception as e:
    helper.init_failure(e)


@helper.create
def create(event, context):
    logger.info("Got a create request.  Going to create an AWS Account")

    mode = event.get("ResourceProperties").get("Mode")

    if mode == "AWS_ORGANIZATIONS":
        account_creation_role_in_root_account_arn = os.environ.get(
            "ACCOUNT_CREATION_ROLE_IN_ROOT_ACCOUNT_ARN"
        )
        organization_account_access_role_name = event.get("ResourceProperties").get("OrganizationAccountAccessRoleName")

        account_name = event.get("ResourceProperties").get("AccountName")
        email = event.get("ResourceProperties").get("Email")
        iam_user_access_to_billing = event.get("ResourceProperties").get(
            "IamUserAccessToBilling"
        )

        with betterboto_client.CrossAccountClientContextManager(
                "organizations",
                account_creation_role_in_root_account_arn,
                "assumable_org_role",
        ) as organizations:
            logger.info("Creating account")
            response = organizations.create_account(
                Email=email,
                AccountName=account_name,
                RoleName=organization_account_access_role_name,
                IamUserAccessToBilling=iam_user_access_to_billing
            )
            create_account_status_id = response.get("CreateAccountStatus").get("Id")
            helper.Data.update({"create_account_status_id": create_account_status_id})


def account_is_ready_to_be_bootstraped(event, target_account_id):
    organization_account_access_role_name = event.get("ResourceProperties").get("OrganizationAccountAccessRoleName")

    with betterboto_client.CrossAccountClientContextManager(
            "codebuild",
            f'arn:aws:iam::{target_account_id}:role/{organization_account_access_role_name}',
            "assumable_org_role_for_codebuild",
    ) as codebuild:
        try:
            result = codebuild.list_projects()
            logger.info(f"Was able to list projects: {result}")
        except Exception as e:
            logger.info(f"Codebuild not available in target account yet: {str(e)}")
            return False
    with betterboto_client.CrossAccountClientContextManager(
            "cloudformation",
            f'arn:aws:iam::{target_account_id}:role/{organization_account_access_role_name}',
            "assumable_org_role_for_cloudformation",
    ) as cloudformation:
        try:
            result = cloudformation.list_stacks()
            logger.info(f"Was able to list stacks: {result}")
            helper.Data.update({"account_ready": True})
            return True
        except Exception as e:
            logger.info(f"Cloudformation not available in target account yet: {str(e)}")
            return False


@helper.poll_create
def poll_create(event, context):
    create_account_status_id = event['CrHelperData'].get("create_account_status_id")

    logger.info(f"Got create poll request.  Checking AWS Account Creation for: {create_account_status_id}")

    account_created = event['CrHelperData'].get("account_created", False)
    account_ready = event['CrHelperData'].get("account_ready", False)
    account_bootstrapped = event['CrHelperData'].get("account_bootstrapped", False)
    account_inflated = event['CrHelperData'].get("account_inflated", False)
    target_account_id = event['CrHelperData'].get("target_account_id", None)

    account_creation_role_in_root_account_arn = os.environ.get(
        "ACCOUNT_CREATION_ROLE_IN_ROOT_ACCOUNT_ARN"
    )

    if not account_created:
        with betterboto_client.CrossAccountClientContextManager(
                "organizations",
                account_creation_role_in_root_account_arn,
                "assumable_org_role",
        ) as organizations:
            create_account_status = organizations.describe_create_account_status(
                CreateAccountRequestId=create_account_status_id
            ).get("CreateAccountStatus")

            state = create_account_status.get("State")
            if state == "IN_PROGRESS":
                return None

            if state == "FAILED":
                raise Exception(create_account_status.get("FailureReason"))

            if state == "SUCCEEDED":
                account_type = event.get("ResourceProperties").get("AccountType")
                account_group = event.get("ResourceProperties").get("AccountGroup")

                with betterboto_client.ClientContextManager('ssm') as ssm:
                    ssm_parameter_name = f"{os.environ.get('SSM_OU_MAP_PREFIX')}/{account_group}/{account_type}"
                    target_ou = ssm.get_parameter(Name=ssm_parameter_name).get("Parameter").get("Value")

                target_account_id = create_account_status.get("AccountId")
                if str(target_ou).startswith("/"):
                    target = organizations.convert_path_to_ou(target_ou)
                else:
                    target = target_ou

                result = organizations.list_parents_single_page(ChildId=target_account_id)
                current_ou = result.get("Parents")[0].get('Id')

                if target != current_ou:
                    organizations.move_account(
                        AccountId=target_account_id,
                        SourceParentId=current_ou,
                        DestinationParentId=target,
                    )

                helper.Data.update(
                    {
                        "account_created": True,
                        "target_account_id": target_account_id,
                    }
                )

    if not account_ready:
        account_ready = account_is_ready_to_be_bootstraped(event, target_account_id)
        helper.Data.update({"account_ready": account_ready})

    if not account_bootstrapped:
        with betterboto_client.ClientContextManager(
                'codebuild',
        ) as codebuild:
            if event['CrHelperData'].get("bootstrap_build_id"):
                logger.info("Checking previously started bootstrapping")
                bootstrap_build_id = event['CrHelperData'].get("bootstrap_build_id")
                response = codebuild.batch_get_builds(ids=[bootstrap_build_id])
                build = response.get('builds')[0]
                build_status = build.get('buildStatus')
                if build_status == 'SUCCEEDED':
                    helper.Data.update({"account_bootstrapped": True})
                elif build_status == "IN_PROGRESS":
                    return None
                else:
                    raise Exception(f"Bootstrapping not succeeded: {build_status}")
            else:
                logger.info("Starting bootstrap")
                organization_account_access_role_name = event.get("ResourceProperties").get(
                    "OrganizationAccountAccessRoleName")
                organization_account_access_role_arn = 'arn:aws:iam::{}:role/{}'.format(
                    target_account_id, organization_account_access_role_name
                )
                response = codebuild.start_build(
                    projectName=os.environ.get('BOOTSTRAPPER_PROJECT_NAME'),
                    environmentVariablesOverride=[
                        {
                            'name': 'ASSUMABLE_ROLE_IN_ROOT_ACCOUNT',
                            'value': os.environ.get('ASSUMABLE_ROLE_IN_ROOT_ACCOUNT_ARN'),
                            'type': 'PLAINTEXT'
                        },
                        {
                            'name': 'ORGANIZATION_ACCOUNT_ACCESS_ROLE_ARN',
                            'value': organization_account_access_role_arn,
                            'type': 'PLAINTEXT'
                        },
                    ],
                )
                helper.Data.update({"bootstrap_build_id": response.get("build").get("id")})
                return None

        if not account_inflated:
            with betterboto_client.ClientContextManager(
                    'codebuild',
            ) as codebuild:
                if event['CrHelperData'].get("inflate_build_id"):
                    logger.info("Checking previously started single account run")
                    inflate_build_id = event['CrHelperData'].get("inflate_build_id")
                    response = codebuild.batch_get_builds(ids=[inflate_build_id])
                    build = response.get('builds')[0]
                    build_status = build.get('buildStatus')
                    if build_status == 'SUCCEEDED':
                        helper.Data.update({"account_inflated": True})
                        return target_account_id
                    elif build_status == "IN_PROGRESS":
                        return None
                    else:
                        raise Exception(f"Single account run not succeeded: {build_status}")
                else:
                    logger.info("Starting single account run")
                    response = codebuild.start_build(
                        projectName='servicecatalog-puppet-single-account-run',
                        environmentVariablesOverride=[
                            {
                                'name': 'SINGLE_ACCOUNT_ID',
                                'value': target_account_id,
                                'type': 'PLAINTEXT'
                            },
                        ]
                    )
                    helper.Data.update(
                        {
                            "inflate_build_id": response.get("build").get("id")
                        }
                    )
                    return None

    return False


@helper.update
def update(event, context):
    logger.info("Got Update")
    # If the update resulted in a new resource being created, return an id for the new resource.
    # CloudFormation will send a delete event with the old id when stack update completes


@helper.poll_update
def poll_update(event, context):
    logger.info("Got update poll")
    # Return a resource id or True to indicate that creation is complete. if True is returned an id
    # will be generated
    return True


@helper.delete
def delete(event, context):
    logger.info("Got Delete")
    # Delete never returns anything. Should not fail if the underlying resources are already deleted.
    # Desired state.


@helper.poll_delete
def poll_delete(event, context):
    logger.info("Got delete poll")
    # Return a resource id or True to indicate that creation is complete. if True is returned an id
    # will be generated
    return True


def handler(event, context):
    helper(event, context)
