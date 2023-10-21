from fastapi import APIRouter, HTTPException, Header, Response

from fastapi import Depends
from typing import Annotated, Any, Optional, Tuple
import jwt
import datetime
import pydantic
from controllers import commons
from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal
from services.commons import base
from controllers import mapper_exceptions

from controllers import management_service_facade
from services import logs
import re
_LOGGER = logs.get_logger()


router = APIRouter()

class CreateCandidateAcademicInfoRequest(BaseModel):
    title : str
    institution : str
    country : base.Country
    year_start_date : int
    month_start_date : int
    year_end_date : Optional[int] = None
    month_end_date: Optional[int] = None
    description : str
    
   
    
    
    
class CreateCandidateRequest(BaseModel):
    document: str
    documentType: base.DocumentType
    firstName: str
    lastName: str
    phoneNumber: str
    username: str
    password: str
    birthDate: str
    age: int
    originCountry: base.Country
    residenceCountry: base.Country
    residenceCity: str
    address: str

class TokenData(BaseModel):
    person_id: str

# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/candidates")
async def create_candidate(request: CreateCandidateRequest, db: Session = Depends(get_db)):
    
    request = management_service_facade.CreateCandidateRequest(document = request.document, document_type = request.documentType,
                                           first_name=request.firstName, last_name = request.lastName, phone_number = request.phoneNumber, username = request.username,\
                                           password = request.password, birth_date = request.birthDate, age = request.age, origin_country= request.originCountry,\
                                           residence_country = request.residenceCountry, residence_city = request.residenceCity, address= request.address)
    
    try:
        management_service_facade.create_candidate(request = request, db = db)
        return {"msg": "Candidate has been created"}
    except (management_service_facade.PersonDocumentAlreadyExistError, management_service_facade.UserNameAlreadyExistError) as e:
        raise HTTPException(status_code=400, detail=e.message)

 
@router.post("/candidates/myself/academic_info")
async def create_candidate_academic_info(request: CreateCandidateAcademicInfoRequest, 
                                         token_data: TokenData = Depends(commons.get_token_data),
                                         db: Session = Depends(get_db)):
    
    try: 
        start_date, end_date = get_dates(request = request)
        academic_request = management_service_facade.CreateCandidateAcademicInfoRequest(person_id =str(token_data.person_id),
                                                                                    title = request.title,
                                                                                    institution = request.institution, 
                                                                                    country = request.country,
                                                                                    start_date = start_date,
                                                                                    end_date = end_date,
                                                                                    description = request.description)
                                                                                    
        management_service_facade.add_candidate_academic_info(request = academic_request, db = db)
        return {"msg": "Candidate academic info has been added"}
          
    
    except  (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as e:
        raise HTTPException(status_code=401) 
    
    except (management_service_facade.ProfessionalDoesNotExistError) as e:
        _LOGGER.error("Error adding academic info [%r]", e)
        mapper_exceptions.process_error_response(exception=e)
    
    
    
        
@router.get("/candidates")
async def get_candidates(response: Response, db: Session = Depends(get_db)):
    candidates_list = management_service_facade.get_candidates(db = db)
    
    if candidates_list is not None:
        data=[]
        for candidate in candidates_list:
            data.append({'document': str(candidate.document),'documentType': str(candidate.document_type)})
        return data
    else:
        _LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No candidates found")
    
    
def get_dates(request: CreateCandidateAcademicInfoRequest)->Tuple[datetime.datetime, Optional[datetime.datetime]]:
    
    month_start_date = request.month_start_date
    year_start_date = request.year_start_date
    
    start_date = datetime.datetime(year_start_date, month_start_date, 1)
    
    month_end_date = request.month_end_date
    year_end_date = request.year_end_date

    end_date = None
    if year_end_date is not None and month_end_date is not None:
        
    
        if month_end_date == 12:
            month_end_date = 1
            year_end_date += 1
        else:
            month_end_date += 1
    
        end_date = datetime.datetime(year_end_date, month_end_date, 1) - datetime.timedelta(days=1)

    return start_date, end_date
    
    