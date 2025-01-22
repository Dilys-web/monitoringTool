import json
from fastapi import APIRouter,Depends
from sqlalchemy.testing import db
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.logs_crud import save_log
from app.services.logs_service import  fetch_platform_logs

router=APIRouter()

@router.get("/")
async def fetch_and_save_logs(db: Session = Depends(get_db)):
   logs= await fetch_platform_logs(["Application"])
   print("startttt")
   print(logs)
   print("enddddd")
   for log in logs[:10]:
       # Serialize the log message if it's a dictionary
        serialized_log = json.dumps(log)  # Assuming log is a dictionary
        await save_log(db, log_source="windows", message=serialized_log, severity="INFO")
   #
   #
   return {"status": "success", "logs_saved": len(logs)}