from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP
from app.core.database import Base
from datetime import datetime

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    log_source = Column(String, index=True)
    severity = Column(String)
    message = Column(Text)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
