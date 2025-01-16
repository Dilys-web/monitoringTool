from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP
from app.core.database import Base
from datetime import datetime

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    log_source = Column(String, index=True)
    log_type = Column(String)
    severity = Column(String)
    message = Column(Text)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    source_ip = Column(String)
    platform = Column(String)
    service_name = Column(String)
    log_metadata = Column(JSON)
    host_name = Column(String)
    cloud_provider = Column(String)
    region = Column(String)
    resource_id = Column(String)