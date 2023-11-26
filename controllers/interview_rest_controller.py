from fastapi import APIRouter, HTTPException ,Response, status

from fastapi import Depends
from typing import Annotated, Any, Optional, Tuple,cast,List
 
from controllers import commons
from pydantic import BaseModel,Field,model_validator

from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal 

from controllers import management_service_facade
from services import logs
import datetime
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
    profile_id: str = Field(min_length=1,max_length=200)
    status : Status
    meet_url : str = Field(min_length=4,max_length=500)
    start_timestamp : datetime.datetime
    duration_minutes: int
    
class AbilityInterviewRequest(BaseModel):
    ability_id: int
    qualification: int
    
class RegisterResultInterviewRequest(BaseModel):
    candidate_document : str = Field(min_length=1,max_length=200)
    project_id : str = Field(min_length=1,max_length=200)
    profile_id: str = Field(min_length=1,max_length=200)
    date : datetime.date 
    recording_file: Optional[str]
    test_file : Optional[str]
    observation: str
    abilities: List[AbilityInterviewRequest]
    
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

@router.get("/interviews")
async def get_interviews(candidate: str|None = None,db: Session = Depends(get_db)):
    
    return [i.dict() for i in  management_service_facade.get_intervies(candidate, db = db)]




@router.post("/interviews/result")
async def load_interview(request: RegisterResultInterviewRequest, db : Session = Depends(get_db))->None:

    
    abilities = list(map(lambda x: management_service_facade.AbilityInterviewRequest(
                                    ability_id = x.ability_id,
                                    qualification= x.qualification), request.abilities))
    
    
    management_service_facade.load_interview(request = management_service_facade.LoadInterviewRequest(
                                                    candidate_document = request.candidate_document,
                                                    project_id=request.project_id,
                                                    profile_id=request.profile_id,
                                                    date  = request.date,
                                                    recording_file = request.recording_file,
                                                    test_file  = request.test_file,
                                                    observation = request.observation,
                                                    abilities=abilities), db=db)
    
    return {"msg": "Candidate interview info has been added"}

@router.get("/interviews/result")
async def find_interview_results( db : Session = Depends(get_db))->None:

    result = management_service_facade.find_interview_results(db)
    return [r.dict() for r in result]


@router.get("/interviews/result/{id}")
async def find_interview_result(id:int, db : Session = Depends(get_db))->None:
    result = management_service_facade.find_interview_result(id,db)
    d = result.dict()
    d.update({"qualification":result.qualification})
    return d

