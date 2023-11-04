from fastapi import APIRouter, HTTPException, Header, Response, status, Request

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
    
class CreateCandidateLaboralInfoRequest(BaseModel):
    position: str
    company_name: str
    company_country: base.Country
    company_address: str
    company_phone: str
    year_start_date : int
    month_start_date : int
    year_end_date : Optional[int] = None
    month_end_date: Optional[int] = None
    description : str
    
class CreateCandidateTechnicalRoleInfoRequest(BaseModel):
    role: str
    experience_years: int
    description : str
    
class CreateCandidateTechnologyInfoRequest(BaseModel):
    name: str
    experience_years: int
    level: int
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

class CandidateSearchRequest(BaseModel):
    roleFilter: Optional[str]
    role: Optional[str]
    roleExperience: Optional[str]
    technologies: Optional[str]
    abilities: Optional[str]
    titleFilter: Optional[str]
    title: Optional[str]
    titleExperience: Optional[str]

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
    except (management_service_facade.PersonDocumentAlreadyExistError, management_service_facade.UserNameAlreadyExistError,\
     management_service_facade.ProfessionalAlreadyExistError) as e:
        raise HTTPException(status_code=400, detail=e.message)

 
@router.post("/candidates/myself/academic_info")
async def create_candidate_academic_info(request: CreateCandidateAcademicInfoRequest, 
                                         token_data: commons.TokenData = Depends(commons.get_token_data),
                                         db: Session = Depends(get_db)):
    
    try: 
        start_date, end_date = get_and_validates_dates(request = request)
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
        
@router.post("/candidates/myself/laboral_info")
async def create_candidate_laboral_info(request: CreateCandidateLaboralInfoRequest, 
                                         token_data: commons.TokenData = Depends(commons.get_token_data),
                                         db: Session = Depends(get_db)):
    
    try: 
        start_date, end_date = get_and_validates_dates(request = request)
        laboral_request = management_service_facade.CreateCandidateLaboralInfoRequest(person_id =str(token_data.person_id),
                                                                                    position = request.position,
                                                                                    company_name = request.company_name,
                                                                                    company_country = request.company_country,
                                                                                    company_address = request.company_address,
                                                                                    company_phone = request.company_phone,
                                                                                    start_date = start_date,
                                                                                    end_date = end_date,
                                                                                    description =request.description)
                                                                                    
        management_service_facade.add_candidate_laboral_info(request = laboral_request, db = db)
        return {"msg": "Candidate laboral info has been added"}
          
    
    except  (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as e:
        raise HTTPException(status_code=401) 
    
    except (management_service_facade.ProfessionalDoesNotExistError, management_service_facade.DateRangeInvalidError) as e:
        _LOGGER.error("Error adding laboral info [%r]", e)
        mapper_exceptions.process_error_response(exception=e)
        
@router.post("/candidates/myself/technical_roles")
async def create_candidate_technical_role(request: CreateCandidateTechnicalRoleInfoRequest, 
                                         token_data: commons.TokenData = Depends(commons.get_token_data),
                                         db: Session = Depends(get_db)):
    
    try: 
        technical_role_info = management_service_facade.CreateCandidateTechnicalRoleInfoRequest(person_id =str(token_data.person_id),
                                                                                    role = request.role,
                                                                                    experience_years = request.experience_years,
                                                                                    description = request.description)
                                                                                    
        management_service_facade.add_candidate_technical_role_info(request = technical_role_info, db = db)
        return {"msg": "Candidate technical role info has been added"}
          
    
    except  (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as e:
        raise HTTPException(status_code=401) 
    
    except (management_service_facade.ProfessionalDoesNotExistError) as e:
        _LOGGER.error("Error adding technical role info [%r]", e)
        mapper_exceptions.process_error_response(exception=e)
        
@router.post("/candidates/myself/technologies")
async def create_technology_info(request: CreateCandidateTechnologyInfoRequest, 
                                         token_data: commons.TokenData = Depends(commons.get_token_data),
                                         db: Session = Depends(get_db)):
    
    try: 
        technology_info_request = management_service_facade.CreateCandidateTechnologyInfoRequest(person_id =str(token_data.person_id),
                                                                                    name = request.name,
                                                                                    experience_years = request.experience_years,
                                                                                    level = request.level,
                                                                                    description = request.description)
                                                                                    
        management_service_facade.add_candidate_technology_info(request = technology_info_request, db = db)
        return {"msg": "Candidate technology info has been added"}
          
    
    except  (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as e:
        raise HTTPException(status_code=401) 
    
    except (management_service_facade.ProfessionalDoesNotExistError) as e:
        _LOGGER.error("Error adding technology info [%r]", e)
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
    
    
def get_and_validates_dates(request: CreateCandidateAcademicInfoRequest)->Tuple[datetime.datetime, Optional[datetime.datetime]]:
    
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
        
    if end_date is not None and end_date < start_date:
        raise management_service_facade.DateRangeInvalidError()

    return start_date, end_date
    
@router.get("/candidates/search")
async def search_for_candidates(request: Request, db: Session = Depends(get_db)):

    technologies=[]
    abilities=[]
    technologies=request.query_params['technologies'].split(',')
    abilities=request.query_params['abilities'].split(',')
    
    request2 = management_service_facade.CandidateSearchRequest(role_filter = request.query_params['roleFilter'],\
     role = request.query_params['role'],  role_experience=request.query_params['roleExperience'],\
     technologies= technologies,\
     abilities= abilities, title_filter=request.query_params['titleFilter'],\
     title=request.query_params['title'],title_experience=request.query_params['titleExperience'])
    
    candidates_list = management_service_facade.search_for_candidates(request=request2, db = db)
    
    if len(candidates_list) > 0:
        data=[]
        for c in candidates_list:
            data.append({'person_id': str(c.person_id),'first_name': str(c.first_name), 'last_name': str(c.last_name),\
             'age:': str(c.age),\
             'roles': c.roles, 'technologies': c.technologies,\
             'titles': c.titles, 'abilities': c.abilities, 'score': c.score })
        return data
    else:
        _LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No candidates found")    