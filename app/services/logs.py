# app/db/crud.py
from sqlalchemy.orm import Session
from app.models.logs import Log
from app.schemas.log_schema import LogCreate

# Create log
def create_log(db: Session, log: LogCreate):
    db_log = Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# Get logs
def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Log).offset(skip).limit(limit).all()

def get_log():
    return {"logger":"Info"}