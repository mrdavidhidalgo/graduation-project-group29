
import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from services.company import company_service
from services.employee import employee_service
from services.user import user_service
from services.person import person_service
from services.professional import professional_service
from daos import db_user_repository, db_person_repository, db_professional_repository, db_employee_repository, db_company_repository
from pydantic import BaseModel
from services.professional.model import professional_model
from services.commons import base

class DateRangeInvalidError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = f"The Range of dates is invalid"
        super().__init__(self.message)

import jwt
class LoginResponse(BaseModel):
    token: str
    username: str

class AuthenticationResponse(BaseModel):
    new_token: str
    username: str
    role:str
    exp:int
    person_id:int
    
UserLoginValidationError = user_service.UserLoginValidationError

UserLoginError = user_service.UserLoginError

UserNameAlreadyExistError = user_service.UserNameAlreadyExistError

PersonDocumentAlreadyExistError = person_service.PersonDocumentAlreadyExistError

UserNameDoesNotExistError = user_service.UserNameDoesNotExistError

ProfessionalDoesNotExistError = professional_service.ProfessionalDoesNotExistError

CompanyTaxprayerAlreadyExistError = company_service.CompanyTaxprayerAlreadyExistError

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
    
class CreateCandidateAcademicInfoRequest(BaseModel):
    person_id : str
    title : str
    institution : str
    country : base.Country
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str
    
class CreateCandidateLaboralInfoRequest(BaseModel):
    person_id : str
    position: str
    company_name: str
    company_country: base.Country
    company_address: str
    company_phone: str
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str

class CreateCompanyRequest(BaseModel):
    document: str
    documentType: str
    firstName: str
    lastName: str
    username: str
    password: str
    taxpayerId: str
    name: str
    country: str
    city: str
    years: str
    address: str
    phoneNumber: str
    profile: str
    position: str
    

######################################################################################################################################
#                                                           USER                                                                     #
######################################################################################################################################

def myself(token:str)->AuthenticationResponse:

    _, map = user_service.myself(token)
        
    return AuthenticationResponse(new_token = token, username=map["user"],
                                  role=map["role"],exp=map["exp"],person_id=map["person_id"]) 

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
    
def add_candidate_academic_info(request: CreateCandidateAcademicInfoRequest, db: Session)->None:
    
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    professional_service.add_academic_info(academic_info=professional_model.ProfessionalAcademicInfo.model_validate(request.model_dump()), 
                                           professional_repository = professional_repository)
    
def add_candidate_laboral_info(request: CreateCandidateLaboralInfoRequest, db: Session)->None:
    
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    professional_service.add_laboral_info(laboral_info=professional_model.ProfessionalLaboralInfo.model_validate(request.model_dump()), 
                                           professional_repository = professional_repository)
                                           

######################################################################################################################################
#                                                       COMPANIES                                                                    #
######################################################################################################################################

def create_company(request: CreateCompanyRequest, db: Session)->None:

    LOGGER.info("Starting Create company with username [%s]", request.username)
    company_repository = db_company_repository.DBCompanyRepository(db = db)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    user_repository = db_user_repository.DBUserRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    
    new_company = company_service.CreateCompanyRequest.model_validate(request.model_dump())
    
    company_service.create_company(request=new_company, 
                                       person_repository=person_repository, 
                                       user_repository=user_repository,
                                       company_repository = company_repository,
                                       employee_repository=employee_repository)

def get_companies(db: Session)->Optional[List[company_service.company_model.Company]]:
    LOGGER.info("Listing all companies")
    company_repository = db_company_repository.DBCompanyRepository(db = db)
    company_list = company_service.get_all(company_repository=company_repository)
    
    if company_list is None:
        LOGGER.info("Empty List in facade")
        return None
    else:
        LOGGER.info("List with data in facade")
        return company_list