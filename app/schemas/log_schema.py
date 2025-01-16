# app/schemas/log_schema.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.core.database import Base

class LogBase(Base):
    log_source: str
    log_type: str
    severity: Optional[str] = None
    message: str
    timestamp: Optional[datetime] = None
    source_ip: Optional[str] = None
    platform: Optional[str] = None
    service_name: Optional[str] = None
    log_metadata: Optional[Dict[str, Any]] = None
    host_name: Optional[str] = None
    cloud_provider: Optional[str] = None
    region: Optional[str] = None
    resource_id: Optional[str] = None

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int

    class Config:
        orm_mode = True
