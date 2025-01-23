import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

def retrieve_aws_logs(log_group: str, start_time: int, end_time: int, aws_access_key: str, aws_secret_key: str):
    try:
        # Create a session with dynamic credentials
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
                "message": event.get("message")
            })

        return logs

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))
