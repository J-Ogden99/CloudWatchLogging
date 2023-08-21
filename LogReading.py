import boto3
import os
import gzip
import shutil

# AWS credentials and region
aws_access_key = "YOUR_ACCESS_KEY"
aws_secret_key = "YOUR_SECRET_KEY"
region_name = "us-east-1"

# Initialize CloudWatch Logs client
client = boto3.client('logs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)

# Log group and log stream names
log_group_name = 'YOUR_LOG_GROUP_NAME'
log_stream_prefix = 'YOUR_LOG_STREAM_PREFIX'
download_directory = 'logs/'

def download_logs(log_group_name, log_stream_name, start_time, end_time, download_directory):
    # Create download directory if it doesn't exist
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startTime=start_time,
        endTime=end_time
    )
    
    log_events = response.get('events', [])
    for event in log_events:
        log_data = event['message']
        
        # Save log data to a file
        log_file_path = os.path.join(download_directory, f"{log_stream_name}.log")
        with open(log_file_path, 'a') as log_file:
            log_file.write(log_data + '\n')

def parse_logs(log_group_name, log_stream_prefix, start_time, download_directory):    
    # List log streams
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        logStreamNamePrefix=log_stream_prefix
    )
    
    log_streams = response.get('logStreams', [])
    for stream in log_streams:
        log_stream_name = stream['logStreamName']
        print(f"Downloading logs from {log_stream_name}")
        download_logs(log_group_name, log_stream_name, start_time, int(stream['lastIngestionTime']), download_directory)

parse_logs(log_group_name, log_stream_prefix, 0, download_directory)
