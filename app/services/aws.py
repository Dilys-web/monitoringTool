import boto3

def retrieve_logs(log_group: str, start_time: str, end_time: str) -> dict:
    client = boto3.client("logs")
    response = client.filter_log_events(
        logGroupName=log_group,
        startTime=int(start_time),
        endTime=int(end_time),
    )
    return {"logs": response.get("events", [])}
