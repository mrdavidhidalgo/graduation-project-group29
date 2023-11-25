from fastapi import APIRouter, HTTPException ,Response, status

from fastapi import Depends
from typing import Annotated, Any, Optional, Tuple,cast,List
 
from controllers import commons
from pydantic import BaseModel,Field,model_validator

from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal 

from controllers import management_service_facade
from services import logs
from datetime import datetime, date
import enum



_LOGGER = logs.get_logger()

router = APIRouter()

class Status(enum.Enum):
    SCHEDULED = "SCHEDULED"
    DONE = "DONE"
    CANCELLED ="CANCELLED"

class CreateInterviewRequest(BaseModel):
    candidate_document : str = Field(min_length=1,max_length=200)
    project_id : str = Field(min_length=1,max_length=200)
    status : Status
    meet_url : str = Field(min_length=4,max_length=500)
    start_timestamp : datetime 
    duration_minutes: int
    

    
# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/interviews")
async def create_interview(request: CreateInterviewRequest,db: Session = Depends(get_db)):
    
    request = management_service_facade.CreateInterviewRequest(**request.copy(exclude={"status"}).dict(),status=request.status.name)
    
    try:
        management_service_facade.create_inverview(request = request, db = db)
        return {"msg": "Interview has been created"}
    except management_service_facade.InterviewAlreadyExistError:
        raise HTTPException(status_code=400, detail="Interview duplicated")

