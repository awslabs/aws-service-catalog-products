# Service Catalog Puppet Logs Exporter

This solution exports the pipeline logs to an S3 bucket in the event that the Service Catalog Pipeline fails, is superseded or is cancelled.

![Template Design](scpuppet-logs.png)

## Description

* Deploys a single product in the tooling account that will trigger Cloudwatch events rule if Service Catalog Puppet pipeline fails
* Triggers a Codebuild project
* Exports logs as a build artifact to an S3 bucket

boto_level = os.environ.get(“BOTO_LOG_LEVEL”, logging.CRITICAL)
logging.getLogger(“boto”).setLevel(boto_level)
logging.getLogger(“boto3”).setLevel(boto_level)
logging.getLogger(“botocore”).setLevel(boto_level)
logging.getLogger(“urllib3”).setLevel(boto_level)
log_level = os.environ.get(“LOG_LEVEL”, logging.WARNING)
logger = logging.getLogger(__name__)
logging.basicConfig(
    format=“%(levelname)s %(threadName)s %(message)s”, level=logging.INFO
)
logger.setLevel(log_level)