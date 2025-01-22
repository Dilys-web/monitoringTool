# app/schemas/log_schema.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.core.database import Base

class LogBase(BaseModel):
    log_source: str
    severity: Optional[str] = None
    message: str
    timestamp: Optional[datetime] = None


class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int

    class Config:
        orm_mode = True
