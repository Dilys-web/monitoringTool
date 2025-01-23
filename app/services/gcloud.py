from google.cloud import logging

def retrieve_logs(log_name: str, start_time: str, end_time: str) -> dict:
    client = logging.Client()
    logger = client.logger(log_name)
    entries = logger.list_entries(filter_=f'timestamp >= "{start_time}" AND timestamp <= "{end_time}"')
    return {"logs": [entry.payload for entry in entries]}
