import boto3, logging, traceback, os
from boto3 import Session

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format='%(levelname)s %(threadName)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO
)


def delete_igw(client, vpc_id):
    fltr = [{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]

    try:
        igw = client.describe_internet_gateways(Filters=fltr)['InternetGateways']

        if igw:
            igw_id = igw[0]['InternetGatewayId']
            client.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
            client.delete_internet_gateway(InternetGatewayId=igw_id)
        return

    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        raise


def delete_subnets(client):
    try:
        subs = client.describe_subnets()['Subnets']

        if subs:
            for sub in subs:
                sub_id = sub['SubnetId']
                client.delete_subnet(SubnetId=sub_id)
        return

    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        raise


def delete_rtbs(client):
    try:
        rtbs = client.describe_route_tables()['RouteTables']

        if rtbs:
            for rtb in rtbs:
                main = False
                for assoc in rtb['Associations']:
                    main = assoc['Main']
                if main:
                    continue
                rtb_id = rtb['RouteTableId']
                client.delete_route_table(RouteTableId=rtb_id)
        return

    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        raise


def delete_acls(client):
    try:
        acls = client.describe_network_acls()['NetworkAcls']

        if acls:
            for acl in acls:
                default = acl['IsDefault']
                if default:
                    continue
                acl_id = acl['NetworkAclId']
                client.delete_network_acl(NetworkAclId=acl_id)
        return

    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        raise


def delete_sgps(client):
    try:
        sgps = client.describe_security_groups()['SecurityGroups']

        if sgps:
            for sgp in sgps:
                default = sgp['GroupName']
                if default == 'default':
                    continue
                sg_id = sgp['GroupId']
                client.delete_security_group(GroupId=sg_id)
        return

    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        raise


def delete_vpc(client, vpc_id, region):
    try:
        client.delete_vpc(VpcId=vpc_id)
        logger.info('VPC {} has been deleted from the {} region.'.format(vpc_id, region))
        return

    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)
        raise


def lambda_handler(e, c):
    account_id=e.get("account_id")
    region=e.get("region")
    role_arn = f"arn:{os.getenv('Partition')}:iam::{account_id}:role/{os.getenv('DeleteDefaultNetworkingRoleNameToAssume')}"
    sts = Session().client('sts')
    assumed_role_object = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="spoke",
    )
    credentials = assumed_role_object['Credentials']
    kwargs = {
        "service_name": "ec2",
        "aws_access_key_id": credentials['AccessKeyId'],
        "aws_secret_access_key": credentials['SecretAccessKey'],
        "aws_session_token": credentials['SessionToken'],
    }
    ec2 = Session().client(**kwargs, region_name=region)

    try:
        attribs = ec2.describe_account_attributes(AttributeNames=['default-vpc'])['AccountAttributes']
        vpc_id = attribs[0]['AttributeValues'][0]['AttributeValue']
        if vpc_id == 'none':
            logger.info('Default VPC not found in {}'.format(region))
            return

        # Since most resources are attached an ENI, this checks for additional resources
        f = [{'Name': 'vpc-id', 'Values': [vpc_id]}]
        eni = ec2.describe_network_interfaces(Filters=f)['NetworkInterfaces']
        if eni:
            logger.error('VPC {} has existing resources in the {} region.'.format(vpc_id, region))
            return

        delete_igw(ec2, vpc_id)
        delete_subnets(ec2)
        delete_rtbs(ec2)
        delete_acls(ec2)
        delete_sgps(ec2)
        delete_vpc(ec2, vpc_id, region)

    except Exception as ex:
        logger.error(ex)
        traceback.print_tb(ex.__traceback__)