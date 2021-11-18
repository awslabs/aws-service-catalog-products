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


def handle(event, context):
    logger.info("starting")
    logger.debug(json.dumps(event, default=str))

    report_name = event.get("ReportName")
    report_definitions = {
            'ReportName': event.get("ReportDefinitionReportName"),
            'TimeUnit': event.get("ReportDefinitionTimeUnit"),
            'Format': event.get("ReportDefinitionFormat"),
            'Compression': event.get("ReportDefinitionCompression"),
            'AdditionalSchemaElements': event.get("ReportDefinitionAdditionalSchemaElements").split("|"),
            'S3Bucket': event.get("ReportDefinitionS3Bucket"),
            'S3Prefix': event.get("ReportDefinitionS3Prefix"),
            'S3Region': event.get("ReportDefinitionS3Region"),
            'AdditionalArtifacts': event.get("ReportDefinitionAdditionalArtifacts").split("|"),
            'RefreshClosedReports': str(event.get("ReportDefinitionRefreshClosedReports")).upper() == "TRUE",
            'ReportVersioning': event.get("ReportDefinitionReportVersioning"),
    }
    parameters = dict(ReportDefinition=report_definitions)

    aws_orgs_cur_read_write_access_role_arn = os.environ.get("AWS_ORGS_CUR_READ_WRITE_ACCESS_ROLE_ARN")
    sts = boto3.client('sts')
    assumed_role_object = sts.assume_role(
        RoleArn=aws_orgs_cur_read_write_access_role_arn,
        RoleSessionName='aws_orgs_cur_read_write_access_role_arn',
    )
    credentials = assumed_role_object['Credentials']
    kwargs = {
        "aws_access_key_id": credentials['AccessKeyId'],
        "aws_secret_access_key": credentials['SecretAccessKey'],
        "aws_session_token": credentials['SessionToken'],
    }
    cur = boto3.client('cur', region_name="us-east-1", **kwargs)
    paginator = cur.get_paginator('describe_report_definitions')
    for page in paginator.paginate():
        for report_definition in page.get("ReportDefinitions", []):
            if report_definition.get("ReportName") == report_name:
                parameters['ReportName'] = report_name
                cur.modify_report_definition(**parameters)
                logger.info("updated")
                return

    cur.put_report_definition(**parameters)
    logger.info("created")


if __name__ == "__main__":
    os.environ['AWS_ORGS_CUR_READ_WRITE_ACCESS_ROLE_ARN'] = 'arn:aws:iam::156551640785:role/platform/CuratedReporting/OrgsRole'
    sample_parameters = dict(
        ReportName="MainCurReport",
        ReportDefinitionReportName="MainCurReport",
        ReportDefinitionTimeUnit="HOURLY",
        ReportDefinitionFormat="Parquet",
        ReportDefinitionCompression="Parquet",
        ReportDefinitionAdditionalSchemaElements="RESOURCES",
        ReportDefinitionS3Bucket="prereqs-finance-account-bucket-1ualbpu2nl5q7",
        ReportDefinitionS3Prefix="Main",
        ReportDefinitionS3Region="eu-west-1",
        ReportDefinitionAdditionalArtifacts="ATHENA",
        ReportDefinitionRefreshClosedReports="True",
        ReportDefinitionReportVersioning="OVERWRITE_REPORT",
    )
    sample_context = None
    handle(sample_parameters, sample_context)
