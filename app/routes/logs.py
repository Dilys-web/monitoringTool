from datetime import datetime
import platform
from typing import List, Optional
import typing
from fastapi import APIRouter, Depends, HTTPException, Query
from requests import Session

from ..models import user_models as models
from ..database import get_db
from .auth import get_current_user
from ..services import local, aws, azure, gcloud, elk
from ..services.local import retrieve_logs

router = APIRouter()




# @router.get("/local")
# def get_local_logs(file_path: str = Query(...)):
#     try:
#         logs = retrieve_logs(file_path)
#         return {"logs": logs}
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="Log file not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
@router.get("/local")
async def get_local_logs(
    log_types:Optional[typing.List[str]] = Query(None, description="List of log types to fetch")):
    try:
        current_platform = platform.system()
        if not log_types:
            if current_platform == "Windows":
                log_types = ["Application"]
            elif current_platform == "Linux":
                log_types = ["syslog"]
            else:
                return {"error": "Unsupported platform"}
            
        logs= await fetch_platform_logs(log_types)
    
        return {"status": "success", "logs_saved": logs}
    except Exception as e:
        return [f"Error fetching  logs: {str(e)}"]
    

@router.get("/aws")
def get_aws_logs(

    log_group: str = Query(..., description="The name of the AWS log group."),
    start_time: str = Query(..., description="Start time in 'YYYY-MM-DDTHH:MM:SS' format."),
    end_time: str = Query(..., description="End time in 'YYYY-MM-DDTHH:MM:SS' format."),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    aws_credentials = db.query(models.AWSCredentials).filter(models.AWSCredentials.user_id == user.id).first()
    if not aws_credentials:
        raise HTTPException(status_code=401, detail="AWS credentials not found")
    aws_access_key , aws_secret_key = aws_credentials.aws_access_key, aws_credentials.aws_secret_key
    print(aws_access_key, aws_secret_key)
    try:
        # Convert start_time and end_time from string to milliseconds
        start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)
        end_timestamp = int(datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)

        if start_timestamp >= end_timestamp:
            raise HTTPException(status_code=400, detail="Start time must be before end time.")

        return aws.retrieve_logs(log_group, start_timestamp, end_timestamp, aws_access_key, aws_secret_key)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use 'YYYY-MM-DDTHH:MM:SS'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/azure")
# def get_azure_logs(resource_id: str, start_time: str, end_time: str):
#     try:
#         return azure.retrieve_logs(resource_id, start_time, end_time)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

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
