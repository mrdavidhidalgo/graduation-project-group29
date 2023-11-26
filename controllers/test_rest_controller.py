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
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"

class CreateTestRequest(BaseModel):
    name : str = Field(min_length=1,max_length=200)
    technology :str= Field(min_length=2,max_length=200)
    duration_minutes : int = Field(gt=0)
    status : Status
    start_date : date 
    end_date: date
    description :str= Field(min_length=1,max_length=5000)
    
    
    @model_validator(mode='after')
    def check_date(self)-> 'CreateTestRequest': 
        if self.start_date>self.end_date :
            raise ValueError('start_date is after end_date')
        return self

class RegisterTestResultRequest(BaseModel):
    test_name : str = Field(min_length=1,max_length=200)
    candidate_document: str = Field(min_length=3,max_length=200)
    points : int = Field(ge=0,le=100)
    observation :str|None= Field(min_length=0,max_length=5000,nullable=True,default=None)


# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tests/results")
async def register_test(request: List[RegisterTestResultRequest],db: Session = Depends(get_db)):

    result = [management_service_facade.RegisterTestResultRequest(**r.dict()) for r in request ]
    try:
        management_service_facade.register_result_tests(request = request, db = db)
        return {"msg": "Test results has been created"}
    except (management_service_facade.TestNameAlreadyExistError):
        raise HTTPException(status_code=400, detail="Test duplicated by name")


@router.post("/tests")
async def create_test(request: CreateTestRequest,token_data: commons.TokenData = Depends(commons.get_token_data),
                      db: Session = Depends(get_db)):
    
    request = management_service_facade.CreateTestRequest(**request.copy(exclude={"status"}).dict(),status=request.status.name)
    
    try:
        management_service_facade.create_test(request = request, db = db)
        return {"msg": "Test has been created"}
    except (management_service_facade.TestNameAlreadyExistError):
        raise HTTPException(status_code=400, detail="Test duplicated by name")


@router.get("/enabled_tests")
async def get_enabled_test(db: Session = Depends(get_db)):
    
    try:
        tests=management_service_facade.get_tests( db = db)
        if tests:
            tests = list(filter(lambda x:x.status, tests))
            return tests
        return []
    except (management_service_facade.TestNameAlreadyExistError):
        raise HTTPException(status_code=404, detail="Test does not found")


@router.get("/technologies")
async def get_technologies(response: Response, db: Session = Depends(get_db)):
    technologies_list = management_service_facade.get_technologies(db = db)
    
    if technologies_list is not None:
        data=[]
        for technology in technologies_list:
            data.append({'technologyId': str(technology.id),'name': str(technology.technology_name),\
             "category": str(technology.category)})
        return data
    else:
        _LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No technologies found")
        
@router.get("/abilities")
async def get_abilities(response: Response, db: Session = Depends(get_db)):
    abilities_list = management_service_facade.get_abilities(db = db)
    
    if abilities_list is not None:
        data=[]
        for ability in abilities_list:
            data.append({'abilityId': str(ability.id),'name': str(ability.ability_name),\
             "category": str(ability.category)})
        return data
    else:
        _LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No technologies found")
