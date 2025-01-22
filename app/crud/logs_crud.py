# crud.py
from sqlalchemy.orm import Session
from app.models.logs import Log

async def save_log(db: Session, log_source: str, message: str,severity:str):
    log = Log(log_source="log_source", message=message,severity=severity)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_logs(db: Session, log_source: str = None):
    return db.query(Log).all()
