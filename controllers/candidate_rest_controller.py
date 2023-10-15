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
    document_type: str
    first_name: str
    last_name: str
    phone_number: str
    username: str
    password: str
    birth_date: str
    age: int
    origin_country: str
    residence_country: str
    residence_city: str
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
    request = management_service_facade.CreateCandidateRequest(document = request.document, document_type = request.document_type,
                                           first_name=request.first_name, last_name = request.last_name, phone_number = request.phone_number, username = request.username,\
                                           password = request.password, birth_date = request.birth_date, age = request.age, origin_country= request.origin_country,\
                                           residence_country = request.residence_country, residence_city = request.residence_city, address= request.address)
    
    try:
        management_service_facade.create_candidate(request = request, db = db)
        return {"msg": "Candidate has been created"}
    except (management_service_facade.PersonDocumentAlreadyExistError, management_service_facade.UserNameAlreadyExistError) as e:
        raise HTTPException(status_code=400, detail=e.message)
    
@router.post("/candidates/myself/academic_info")
async def create_candidate_academic_info(request: CreateCandidateAcademicInfoRequest, db: Session = Depends(get_db)):
    print(f"hola {request}")
    academic_request = management_service_facade.CreateCandidateAcademicInfoRequest(person_id =request.person_id,
                                                                                    title = request.title,
                                                                                    institution = request.institution, 
                                                                                    country = request.country,
                                                                                    start_date = request.start_date,
                                                                                    end_date = request.end_date,
                                                                                    description = request.description)
    print(f"salida {request}")
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