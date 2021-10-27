# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved. 
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 
##################################################################################

import json, logging, os
import boto3
import traceback

from urllib.request import Request, urlopen
from time import sleep

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format='%(levelname)s %(threadName)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO
)

try:
    logger.info("Container initialization completed")
except Exception as e:
    logger.error(e, exc_info=True)
    init_failed = e


############################################################ 
#                 ASSOCIATION FUNCTIONS                    #
############################################################ 

def get_account_email(root_org_client, root_role, spoke_id):
    """
    Retrieves the email address associated to the Spoke account
    :param root_org_client: The Organizations client for the Root account
    :param root_role: The role in the Org master to assume into
    :param spoke_id: The account number for the spoke
    :return: The email address associated to the spoke account
    """
    try:
        account_info = root_org_client.describe_account(AccountId=spoke_id)
        email = account_info['Account']['Email']
        logger.info("Email found for account {}: {}".format(spoke_id, email))
        return email
    except Exception as e:
        logger.error("Unable to find email for account: {}".format(e))
        raise
        

def find_create_detector_spoke():
    """
    Finds existing detectors in the spoke or creates one if it does not already exist
    :return: The ID of the detector in the spoke account
    """
    spoke_guardduty = boto3.client('guardduty')
    try:
        logger.info('Finding Spoke Detector ID...')
        list_spoke_detectors = spoke_guardduty.list_detectors()
        spoke_detector = list_spoke_detectors['DetectorIds']
        if not spoke_detector:
            logger.info('Detector not found, creating one...')
            create_spoke_detector = spoke_guardduty.create_detector(
                Enable=True,
                FindingPublishingFrequency='FIFTEEN_MINUTES'
            )
            spoke_detector_id = create_spoke_detector['DetectorId']
            logger.info("Created detector with ID {}".format(spoke_detector_id))
            return spoke_detector_id
        elif len(spoke_detector) > 1:
            logger.error("Too many detectors found! List of detectors: {}".format(spoke_detector))
            raise ValueError("Too many detectors")
        else:
            spoke_detector_id = spoke_detector[0]
            logger.info("Detector already exists: {}".format(spoke_detector_id))
            return spoke_detector_id
    except Exception as e:
        logger.error('Unable to find/create the detector: {}'.format(e))
        raise
    

def find_create_detector_hub(hub_gd):
    """
    Finds existing detectors in the hub or creates one if it does not already exist
    :param hub_gd: The GuardDuty client for the Hub account
    :return: The ID of the detector found in the Hub account
    """
    logger.info('Finding Hub detector ID...')
    try:
        list_hub_detectors = hub_gd.list_detectors()
        hub_detector = list_hub_detectors['DetectorIds']
        if not hub_detector:
            logger.info('Detector not found, creating one...')
            create_hub_detector = hub_gd.create_detector(
                Enable=True,
                FindingPublishingFrequency='FIFTEEN_MINUTES'
            )
            hub_detector = create_hub_detector['DetectorId']
            logger.info("Created detector of ID {} in the Hub account".format(hub_detector))
            return hub_detector
        elif len(hub_detector) > 1:
            logger.error("Too many detectors found! List of detectors: {}".format(hub_detector))
            raise ValueError("Too many detectors")
        else:
            logger.info("Detector found with ID {}".format(hub_detector[0]))
            return hub_detector[0]
    except Exception as e:
        logger.error('Unable to find/create the detector: {}'.format(e))
        raise


def create_member_in_hub(hub_gd, hub_detect_id, spoke_id, spoke_email):
    """
    Creates member accounts of the Hub account
    :param hub_gd: The GuardDuty client for the Hub account
    :param hub_detect_id: The ID for the GuardDuty detector in the Hub account
    :param spoke_id: The ID of the spoke account
    :param spoke_email: The email associated to the Spoke account
    """
    try:
        logger.info('Attempting to create member')
        hub_gd.create_members(
            AccountDetails=[
                {
                    'AccountId': spoke_id,
                    'Email': spoke_email
                }
            ],
            DetectorId=hub_detect_id)
        return 
    except Exception as e:
        logger.error("Unable to create members for GuardDuty in the Hub account: {}".format(e))
        raise


def invite_detector_from_hub(hub_gd, hub_detector, spoke_detector, spoke_id, hub_id):
    """
    Invites spoke detectors to join GuardDuty from the Hub account
    :param hub_gd: The GuardDuty client for the Hub account
    :param spoke_gd: The GuardDuty client for the Spoke account
    :param hub_detector: The ID for the GuardDuty detector in the Hub account
    :param spoke_detector: The ID for the GuardDuty detector in the Spoke account
    :param spoke_id: The ID of the spoke account
    :param hub_id: The ID of the Hub account
    :return: Response status
    """
    try:
        logger.info('Checking whether the Spoke Detector Id is the same as the Hub DetectorId')
        if hub_detector != spoke_detector:
            logger.info("Attempting to invite spoke account {} from detector {} in Hub account".format(spoke_id, hub_detector))
            hub_gd.invite_members(
                AccountIds=[
                    spoke_id,
                ],
                DetectorId=hub_detector,
                DisableEmailNotification=False,
                Message="Account {} has been invited to join GuardDuty in the Hub Account ({})".format(spoke_id, hub_id))

            return accept_invitation_from_spoke(hub_id, spoke_detector)
        else:
            logger.info('No action needed as Spoke is the Hub')
            return 'SUCCESS'
    except Exception as e:
        logger.error("Unable to invite the detector from the Hub: {}".format(e))
        raise e


def accept_invitation_from_spoke(hub_acc_id, spoke_detector_id):
    """
    Invites spoke detectors to join GuardDuty from the Hub account
    :param guardduty: The GuardDuty client for the Spoke account
    :param hub_acc_id: The ID for the GuardDuty detector in the Hub account
    :param spoke_detector_id: The ID for the GuardDuty detector in the Spoke account
    :return: The ID of the detector found in the Hub account
    """
    guardduty = boto3.client('guardduty') 

    try:
        logger.info('Searching for Invitation in Spoke account...')
        invite_list = {'Invitations': []}
        # Guard against attempting to accept invitations too early
        # Willing to wait up to 90 seconds for invitations to appear
        break_counter = 0
        while not invite_list['Invitations'] and break_counter < 18:
            sleep(5) 
            break_counter += 1
            invite_list = guardduty.list_invitations()
        
        # If list is empty at the end of 1 minute
        if not invite_list['Invitations']:
            logger.error('No invitations found')
            return 'FAILED'

        for invite in invite_list['Invitations']:
            if invite['AccountId'] == hub_acc_id:
                logger.info('Invitation from Hub account found: {}'.format(invite))
                invitation_id = invite['InvitationId']
                guardduty.accept_invitation(DetectorId=spoke_detector_id, InvitationId=invitation_id, MasterId=hub_acc_id)
                logger.info('Account added to hub account')
                return 'SUCCESS'
        logger.error('No match found')
        return 'FAILED'

    except Exception as e:
        logger.error('Could not accept invitations: {}'.format(e))
        raise
    finally:
        logger.info('FINISHED')


############################################################ 
#                   PRIMARY FUNCTIONS                      #
############################################################ 

def disassociate_guardduty(hub_account_id):
    spoke_guardduty = boto3.client('guardduty')
    try:
        logger.info('Finding Spoke Detector ID')
        listSpokeDetectors = spoke_guardduty.list_detectors()
        spoke_detector = listSpokeDetectors['DetectorIds']
        if not spoke_detector:
            logger.error('Detector Not Found')
            return "FAILED"
        else:
            logger.info("Detector found: {}".format(spoke_detector))
            for detector_id in spoke_detector:
                spoke_guardduty.disassociate_from_master_account(DetectorId=detector_id)

            invite_list = spoke_guardduty.list_invitations()
            for invite in invite_list['Invitations']:
                if invite['AccountId'] == hub_account_id:
                    invitation_id = invite['InvitationId']
                    logger.info('Invitation found: {}'.format(invitation_id))
                    spoke_guardduty.delete_invitations(AccountIds=[hub_account_id])
                    return "SUCCESS"
                else:
                    logger.error('No invitations found')
                    return "FAILED"
    except Exception as e:
        logger.error('The request is rejected: {}'.format(e))
        raise


def associate_guardduty(spoke_account_id, root_org_role, hub_guardduty_role, hub_account_id):
    sts = boto3.client('sts')
    organizations = sts.assume_role(RoleArn=root_org_role, RoleSessionName='OrganizationsSearch')
    root_of_org_credentials = organizations['Credentials']
    root_of_org_organizations_client = boto3.client(
        'organizations',
        aws_access_key_id=root_of_org_credentials['AccessKeyId'],
        aws_secret_access_key=root_of_org_credentials['SecretAccessKey'],
        aws_session_token=root_of_org_credentials['SessionToken'],
    )

    assume_hub_account = sts.assume_role(RoleArn=hub_guardduty_role, RoleSessionName='SpokeGuardDuty')
    hub_credentials = assume_hub_account['Credentials']
    hub_guardduty = boto3.client(
        'guardduty',
        aws_access_key_id=hub_credentials['AccessKeyId'],
        aws_secret_access_key=hub_credentials['SecretAccessKey'],
        aws_session_token=hub_credentials['SessionToken'],
    )

    hub_detector_id =  find_create_detector_hub(hub_guardduty)
    spoke_detector_id = find_create_detector_spoke()

    logger.info('Searching Organization for Spoke email...')
    spoke_email = get_account_email(root_of_org_organizations_client, root_org_role, spoke_account_id)
    create_member_in_hub(hub_guardduty, hub_detector_id, spoke_account_id, spoke_email)

    return invite_detector_from_hub(hub_guardduty, hub_detector_id, spoke_detector_id, spoke_account_id, hub_account_id)


############################################################ 
#                     HELPER FUNCTION                      #
############################################################ 

def send_response(e, c, rs, rd):
    """
    Packages response and send signals to CloudFormation
    :param e: The event given to this Lambda function
    :param c: Context object, as above
    :param rs: Returned status to be sent back to CFN
    :param rd: Returned data to be sent back to CFN
    """
    logger.info("Sending response: {}".format(rs))
    r = json.dumps({
        "Status": rs,
        "Reason": "CloudWatch Log Stream: " + c.log_stream_name,
        "PhysicalResourceId": c.log_stream_name,
        "StackId": e['StackId'],
        "RequestId": e['RequestId'],
        "LogicalResourceId": e['LogicalResourceId'],
        "Data": rd
    })
    d = str.encode(r)
    h = {
        'content-type': '',
        'content-length': str(len(d))
    }
    req = Request(e['ResponseURL'], data=d, method='PUT', headers=h)
    r = urlopen(req)
    logger.info("Status message: {} {}".format(r.msg, r.getcode()))


############################################################ 
#                LAMBDA FUNCTION HANDLER                   #
############################################################ 
# IMPORTANT: The Lambda function will be called whenever   #
# changes are made to the stack. Thus, ensure that the     #
# signals are handled by your Lambda function correctly,   #
# or the stack could get stuck in the DELETE_FAILED state  #
############################################################

def handler(event, context):
    """
    Entrypoint to Lambda
    :param event: event passed to the Lambda handler from CloudFormation
    :param context: contains information about the Lambda function
    """
    request_type = event['RequestType']
    logger.info("Received an event of type {} from CloudFormation".format(request_type))
    
    hub_account_id = event['ResourceProperties']['HubAccountId']
    try:
        if request_type == 'Create':
            spoke_account_id = event['ResourceProperties']['SpokeAccountID']
            root_org_role = event['ResourceProperties']['GuardDutyAssumableOrgRoleArn']
            hub_guardduty_role = event['ResourceProperties']['AssumableHubRoleArn']
            response_status = associate_guardduty(spoke_account_id, root_org_role, hub_guardduty_role, hub_account_id)
            send_response(event, context, response_status, {"Message": "Created"})
        elif request_type == 'Delete':
            response_status = disassociate_guardduty(hub_account_id)
            send_response(event, context, response_status, {"Message": "Deleted"})
        elif request_type == 'Update':
            logger.info('Update Requests are not supported: Delete Product and redeploy to make changes')
            send_response(event, context, "FAILED", {"Message": "Unsupported"})
    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        send_response(
            event,
            context,
            "FAILED",
            {
                "Message": "Exception"
            }
        )
