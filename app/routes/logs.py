from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from ..services import local, aws, azure, gcloud, elk
from ..services.local import retrieve_logs

router = APIRouter()




@router.get("/local")
def get_local_logs(file_path: str = Query(...)):
    try:
        logs = retrieve_logs(file_path)
        return {"logs": logs}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Log file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/aws")
def get_aws_logs(
    log_group: str = Query(..., description="The name of the AWS log group."),
    start_time: str = Query(..., description="Start time in 'YYYY-MM-DDTHH:MM:SS' format."),
    end_time: str = Query(..., description="End time in 'YYYY-MM-DDTHH:MM:SS' format.")
):
    try:
        # Convert start_time and end_time from string to milliseconds
        start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)
        end_timestamp = int(datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)

        if start_timestamp >= end_timestamp:
            raise HTTPException(status_code=400, detail="Start time must be before end time.")

        return aws.retrieve_logs(log_group, start_timestamp, end_timestamp)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use 'YYYY-MM-DDTHH:MM:SS'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/azure")
def get_azure_logs(resource_id: str, start_time: str, end_time: str):
    try:
        return azure.retrieve_logs(resource_id, start_time, end_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gcloud")
def get_gcloud_logs(log_name: str, start_time: str, end_time: str):
    try:
        return gcloud.retrieve_logs(log_name, start_time, end_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/elk")
def get_elk_logs(index: str, query: dict):
    try:
        return elk.retrieve_logs(index, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
