from typing import Optional, List
from fastapi import Depends, FastAPI, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import get_db
from .routes.auth import verify_password, create_access_token 
from . import models, schemas
from .routes.auth import router as auth_router
from .routes.logs import router as logs_router
from .services import local, aws
import uvicorn
from .models import user_models
from datetime import datetime

app = FastAPI()

app.include_router(logs_router, prefix="/logs", tags=["Logs"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(auth_router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Monitoring API"}

@app.post("/token", response_model=schemas.Token)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(user_models.User).filter(user_models.User.email == data.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    if not verify_password(data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/query")
def query_logs(
    log_source: str = Query(..., description="Source of logs: 'local' or 'aws'."),
    file_path: Optional[str] = Query(None, description="Path to log file (if source is 'local')."),
    start_time: Optional[str] = Query(None, description="Start time in 'YYYY-MM-DDTHH:MM:SS' format."),
    end_time: Optional[str] = Query(None, description="End time in 'YYYY-MM-DDTHH:MM:SS' format."),
    log_level: Optional[str] = Query(None, description="Log level (e.g., INFO, ERROR, DEBUG)."),
    keywords: Optional[List[str]] = Query(None, description="Keywords to search for in logs."),
    aggregate_by: Optional[str] = Query(None, description="Aggregation metric (e.g., 'count', 'average')."),
    aws_access_key: Optional[str] = Query(None, description="AWS access key (if source is 'aws')."),
    aws_secret_key: Optional[str] = Query(None, description="AWS secret key (if source is 'aws').")
):
    try:
        start_timestamp, end_timestamp = convert_timestamps(start_time, end_time)
        logs = fetch_logs(log_source, file_path, start_timestamp, end_timestamp, aws_access_key, aws_secret_key)
        logs = filter_logs(logs, log_level, keywords)
        return aggregate_logs(logs, aggregate_by)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use 'YYYY-MM-DDTHH:MM:SS'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def convert_timestamps(start_time: Optional[str], end_time: Optional[str]):
    start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000) if start_time else None
    end_timestamp = int(datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000) if end_time else None
    return start_timestamp, end_timestamp

def fetch_logs(log_source: str, file_path: Optional[str], start_timestamp: Optional[int], end_timestamp: Optional[int], aws_access_key: Optional[str], aws_secret_key: Optional[str]):
    if log_source == "aws":
        if not aws_access_key or not aws_secret_key:
            raise HTTPException(status_code=400, detail="AWS credentials are required for AWS logs.")
        return aws.retrieve_logs(log_group="your-log-group", start_time=start_timestamp, end_time=end_timestamp, aws_access_key=aws_access_key, aws_secret_key=aws_secret_key)
    elif log_source == "local":
        if not file_path:
            raise HTTPException(status_code=400, detail="File path is required for local logs.")
        return local.retrieve_logs(file_path)
    else:
        raise HTTPException(status_code=400, detail="Invalid log source.")

def filter_logs(logs: List[dict], log_level: Optional[str], keywords: Optional[List[str]]):
    if log_level:
        logs = [log for log in logs if log.get("level", "").upper() == log_level.upper()]
    if keywords:
        logs = [log for log in logs if any(keyword.lower() in log.get("message", "").lower() for keyword in keywords)]
    return logs

def aggregate_logs(logs: List[dict], aggregate_by: Optional[str]):
    if aggregate_by:
        if aggregate_by == "count":
            return {"aggregation": len(logs)}
        elif aggregate_by == "average":
            timestamps = [log.get("timestamp") for log in logs if "timestamp" in log]
            if len(timestamps) > 1:
                avg_time_diff = sum([timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]) / (len(timestamps) - 1)
                return {"aggregation": avg_time_diff}
            return {"aggregation": "Not enough data for average time calculation"}
        else:
            raise HTTPException(status_code=400, detail="Invalid aggregation metric. Use 'count' or 'average'.")
    return {"logs": logs}

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)