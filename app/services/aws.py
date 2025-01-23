import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

def retrieve_logs(log_group, start_time, end_time, aws_access_key, aws_secret_key):
    try:
        # Create a session using provided AWS credentials
        session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

        # Create a CloudWatch Logs client
        client = session.client('logs')

        # Filter log events
        response = client.filter_log_events(
            logGroupName=log_group,
            startTime=start_time,
            endTime=end_time
        )

        logs = []
        for event in response.get('events', []):
            logs.append({
                "timestamp": event.get("timestamp"),
                "message": event.get("message"),
                "source": event.get("logStreamName"),
                "level": event.get("logLevel")
            })

        return logs

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")