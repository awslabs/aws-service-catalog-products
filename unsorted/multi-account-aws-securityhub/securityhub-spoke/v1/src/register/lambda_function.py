# Any code, applications, scripts, templates, proofs of concept, documentation
# and other items provided by AWS under this SOW are "AWS Content,"" as defined
# in the Agreement, and are provided for illustration purposes only. All such
# AWS Content is provided solely at the option of AWS, and is subject to the
# terms of the Addendum and the Agreement. Customer is solely responsible for
# using, deploying, testing, and supporting any code and applications provided
# by AWS under this SOW.
#
# (c) 2019 Amazon Web Services

import logging
import json
import boto3
import cfnresponse

# Configure logging
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
if len(logging.getLogger().handlers) > 0:
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(format=FORMAT, level=logging.INFO)

def lambda_handler(event, context):
    """ Lambda Function for command execution """
    logging.info(json.dumps(event, indent=2))
    request_type = event['RequestType']
    if request_type == 'Create':
        associate_securityhub(event, context)
    elif request_type == 'Delete':
        disassociate_securityhub(event, context)

def assume_role(arn, session_name):
    """aws sts assume-role --role-arn arn:aws:iam::00000000000000:role/example-role --role-session-name example-role"""

    sts_client = boto3.client('sts')
    sts_client.get_caller_identity()["Account"]

    response = sts_client.assume_role(
        RoleArn=arn, RoleSessionName=session_name)

    session = boto3.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                            aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                            aws_session_token=response['Credentials']['SessionToken'])

    return session

def associate_securityhub(event, context):
    status = cfnresponse.FAILED
    data = {}

    try:
        create_invite_member(event)
        accept_invite(event)
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        logging.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=None)

def create_invite_member(event):

    arn = event['ResourceProperties']['AssumableHubRoleArn']
    spoke_account_id = event['ResourceProperties']['SpokeAccountId']
    email = event['ResourceProperties']['Email']

    session = assume_role(arn, 'SecurityHubInvite')

    logging.info("Creating Member")

    client = session.client('securityhub')
    create_response = client.create_members(
        AccountDetails=[
            {
                'AccountId': spoke_account_id,
                'Email': email
            },
        ]
    )

    logging.info(create_response)

    logging.info("Inviting Member")
    invite_response = client.invite_members(
        AccountIds=[
            spoke_account_id,
        ]
    )

    logging.info(invite_response)

def accept_invite(event):

    HubAccountId = event['ResourceProperties']['HubAccountId']
    
    client = boto3.client('securityhub')

    resp = client.list_invitations()
    items = []
    while resp:
        items += resp['Invitations']
        resp = client.list_invitations()(NextToken=resp['NextToken']) if 'NextToken' in resp else None

    logging.info("Invites received in total")
    logging.info(items)

    invite_id = None

    for item in items:
        if item['AccountId'] == HubAccountId:
            logging.info("Success. Invite Received from Hub Security account.")
            invite_id = item['InvitationId']
            logging.info(item)
        else:
            logging.error("Cannot find invite from Hub Security account.")
            raise Exception
    
    accept_response = client.accept_invitation(
        MasterId=HubAccountId,
        InvitationId=invite_id
    )

    logging.info("Accepted Invitation")
    logging.info(accept_response)


def disassociate_securityhub(event, context):
    status = cfnresponse.FAILED
    data = {}

    try:
        delete_member(event)
        status = cfnresponse.SUCCESS

    except BaseException as ex:
        logging.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=None)

def delete_member(event):
    
    spoke_account_id = event['ResourceProperties']['SpokeAccountId']
    arn = event['ResourceProperties']['AssumableHubRoleArn']

    session = assume_role(arn, 'SecurityHubInvite')
    
    logging.info("Disassociating Member")

    client = session.client('securityhub')

    response = client.disassociate_members(
        AccountIds=[
            spoke_account_id,
        ]
    )

    logging.info(response)

    logging.info("Deleting Member")
    
    delete_response = client.delete_members(
        AccountIds=[
            spoke_account_id,
        ]
    )
    logging.info(delete_response)
