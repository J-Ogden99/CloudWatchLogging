import boto3
import logging
import time

# Create a CloudWatch Logs client
client = boto3.client('logs')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log_request(**kwargs):
    # Construct the log message
    if 'version' not in kwargs or 'product_no' not in kwargs or 'format' not in kwargs:
        return
    message = f'{kwargs["version"]}_{kwargs["product_no"]}_{kwargs["format"]}'
    if 'region_no' in kwargs:
        message += f'_{kwargs["region_no"]}'
    if 'link_no' in kwargs:
        message += f'_{kwargs["link_no"]}'
    if 'source' in kwargs:
        message += f'_{kwargs["source"]}'
    else:
        message += '_2'

    # Send the log message to CloudWatch
    response = client.put_log_events(
        logGroupName='data-service-queries-group',
        logStreamName='data-service-queries-stream',
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': message
            }
        ]
    )

    # Print the response from CloudWatch
    print(response)
