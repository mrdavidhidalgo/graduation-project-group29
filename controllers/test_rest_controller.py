from fastapi import APIRouter, HTTPException, Header, Response

from fastapi import Depends
from typing import Annotated, Any, Optional, Tuple,cast
import jwt
import datetime
import pydantic
from controllers import commons
from pydantic import BaseModel,Field,model_validator

from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal
from services.commons import base
from controllers import mapper_exceptions

from controllers import management_service_facade
from services import logs
from datetime import datetime, date




_LOGGER = logs.get_logger()

router = APIRouter()

class CreateTestRequest(BaseModel):
    name : str = Field(min_length=1,max_length=200)
    technology :str= Field(min_length=2,max_length=200)
    duration_minutes : int = Field(gt=0)
    status : bool
    start_date : date 
    end_date: date
    description :str= Field(min_length=1,max_length=5000)
    
    
    @model_validator(mode='after')
    def check_date(self)-> 'CreateTestRequest': 
        if self.start_date>self.end_date :
            raise ValueError('start_date is after end_date')
        return self

# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tests")
async def create_test(request: CreateTestRequest,token_data: commons.TokenData = Depends(commons.get_token_data),
                      db: Session = Depends(get_db)):
    
    request = management_service_facade.CreateTestRequest(**request.dict())
    
    try:
        management_service_facade.create_test(request = request, db = db)
        return {"msg": "Test has been created"}
    except (management_service_facade.TestNameAlreadyExistError):
        raise HTTPException(status_code=400, detail="Test duplicated by name")

    