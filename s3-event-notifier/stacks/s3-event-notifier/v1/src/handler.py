import json
import logging

# Configure logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

'''
Function to process the event
'''


def handler(event, context):
    LOGGER.debug(json.dumps(event, indent=4, default=str))

    data = {}

    try:
        # Fetch the message records
        records_ = event['Records']

        for sqs_record in records_:

            # The body of the SQS message is a text, hence converting it into a python dictionary
            s3_event_string = sqs_record['body']
            s3_event = json.loads(s3_event_string)

            for s3_record in s3_event['Records']:
                data['bucketName'] = s3_record['s3']['bucket']['name']
                data['key'] = s3_record['s3']['object']['key']
                data['eventTime'] = s3_record['eventTime']
    except BaseException as ex:
        raise ex
    finally:
        LOGGER.debug(json.dumps(data, indent=4, default=str))
        return data
