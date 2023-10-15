import datetime
from fastapi import APIRouter, HTTPException, Header, Response, status

from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Annotated, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal

from controllers import management_service_facade
from services import logs
LOGGER = logs.get_logger()

router = APIRouter()

class CreateCandidateAcademicInfoRequest(BaseModel):
    person_id : str
    title : str
    institution : str
    country : str
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str
    
class CreateCandidateRequest(BaseModel):
    document: str
    documentType: str
    firstName: str
    lastName: str
    phoneNumber: str
    username: str
    password: str
    birthDate: str
    age: int
    originCountry: str
    residenceCountry: str
    residenceCity: str
    address: str

    
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
async def create_candidate_academic_info(request: CreateCandidateAcademicInfoRequest, db: Session = Depends(get_db)):
    
    academic_request = management_service_facade.CreateCandidateAcademicInfoRequest(person_id =request.person_id,
                                                                                    title = request.title,
                                                                                    institution = request.institution, 
                                                                                    country = request.country,
                                                                                    start_date = request.start_date,
                                                                                    end_date = request.end_date,
                                                                                    description = request.description)
    try:
        management_service_facade.add_candidate_academic_info(request = academic_request, db = db)
        return {"msg": "Candidate academic info has been added"}
    except (management_service_facade.ProfessionalDoesNotExistError) as e:
        raise HTTPException(status_code=400, detail=e.message)
    
        
@router.get("/candidates")
async def get_candidates(response: Response, db: Session = Depends(get_db)):
    candidates_list = management_service_facade.get_candidates(db = db)
    
    if candidates_list is not None:
        data=[]
        for candidate in candidates_list:
            data.append({'document': str(candidate.document), 'documentType': str(candidate.documentType)})
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No candidates found")