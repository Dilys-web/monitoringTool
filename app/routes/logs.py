from fastapi import APIRouter, HTTPException
from ..services import local, aws, azure, gcloud, elk

router = APIRouter()

@router.get("/local")
def get_local_logs(file_path: str):
    try:
        return local.retrieve_logs(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/aws")
def get_aws_logs(log_group: str, start_time: str, end_time: str):
    try:
        return aws.retrieve_logs(log_group, start_time, end_time)
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
