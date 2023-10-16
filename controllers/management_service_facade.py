
import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from services.user import user_service
from services.person import person_service
from services.professional import professional_service
from daos import db_user_repository, db_person_repository, db_professional_repository
from pydantic import BaseModel
from services.professional.model import professional_model

class LoginResponse(BaseModel):
    token: str
    username: str
    
UserLoginValidationError = user_service.UserLoginValidationError

UserLoginError = user_service.UserLoginError

UserNameAlreadyExistError = user_service.UserNameAlreadyExistError

PersonDocumentAlreadyExistError = person_service.PersonDocumentAlreadyExistError

UserNameDoesNotExistError = user_service.UserNameDoesNotExistError

ProfessionalDoesNotExistError = professional_service.ProfessionalDoesNotExistError

#LOGGER = user_service.LOGGER
from services import logs
LOGGER = logs.get_logger()

    
class LoginRequest(BaseModel):
    username: str
    password: str
    
class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str
    person: int

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
    
class CreateCandidateAcademicInfoRequest(BaseModel):
    person_id : str
    title : str
    institution : str
    country : str
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str

def login(login_request: LoginRequest, db: Session)->LoginResponse:
    
    user_repository = db_user_repository.DBUserRepository(db = db)
    
    token = user_service.login_user(user_repository=user_repository, username=login_request.username, password=login_request.password)
    
    return LoginResponse(token = token, username=login_request.username) 

def create_user(request: CreateUserRequest, db: Session)->None:
    
    user_repository = db_user_repository.DBUserRepository(db = db)
    
    user_service.create_user(user_repository=user_repository, username=request.username, password=request.password, role=request.role, person = request.person)
    

######################################################################################################################################
#                                                       CANDIDATE                                                                    #
######################################################################################################################################

def create_candidate(request: CreateCandidateRequest, db: Session)->None:

    LOGGER.info("Starting Create candidate with username [%s]", request.username)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    user_repository = db_user_repository.DBUserRepository(db = db)
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    new_request = person_service.CreateCandidateRequest.model_validate(request.model_dump())
    
    person_service.create_candidate(request=new_request, 
                                       person_repository=person_repository, 
                                       user_repository=user_repository,
                                       professional_repository=professional_repository)

def get_candidates(db: Session)->List[person_service.person_model.Person]:
    LOGGER.info("Listing all candidates")
    person_repository = db_person_repository.DBPersonRepository(db = db)
    professional_list = person_service.get_all(person_repository=person_repository)
    
    if professional_list is None:
        LOGGER.info("Empty List in facade")
        return []
    else:
        LOGGER.info("List with data in facade")
        return professional_list
    
# En el token debe venir el person_id
def add_candidate_academic_info(request: CreateCandidateAcademicInfoRequest, db: Session)->None:
    
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    professional_service.add_academic_info(academic_info=professional_model.ProfessionalAcademicInfo.model_validate(request.model_dump()), 
                                           professional_repository = professional_repository)