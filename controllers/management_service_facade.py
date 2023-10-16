
from sqlalchemy.orm import Session
from services.user import user_service
from services.person import person_service
from services.professional import professional_service
from daos import db_user_repository, db_person_repository, db_professional_repository
from pydantic import BaseModel
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

class CreateProfessionalRequest(BaseModel):
    document: int
    documentType: str
    firstName: str
    lastName: str
    phoneNumber: str
    username: str
    password: str
    role: str
    birthDate: str
    age: int
    originCountry: str
    residenceCountry: str
    residenceCity: str
    address: str

def myself(token:str)->AuthenticationResponse:

    map = user_service.myself(token)
        
    return AuthenticationResponse(new_token = token, username=map["user"],
                                  role=map["role"],exp=map["exp"],person_id=map["person_id"]) 

def login(login_request: LoginRequest, db: Session)->LoginResponse:
    
    user_repository = db_user_repository.DBUserRepository(db = db)
    
    token = user_service.login_user(user_repository=user_repository, username=login_request.username, password=login_request.password)
    
    return LoginResponse(token = token, username=login_request.username) 

def create_user(request: CreateUserRequest, db: Session)->None:
    
    user_repository = db_user_repository.DBUserRepository(db = db)
    
    user_service.create_user(user_repository=user_repository, username=request.username, password=request.password, role=request.role, person = request.person)

def create_professional(request: CreateProfessionalRequest, db: Session)->None:

    LOGGER.info("Starting Create Professional with role [%d]", request.role)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    user_repository = db_user_repository.DBUserRepository(db = db)
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    person_service.create_professional(document = request.document, documentType= request.documentType,
                                           firstName=request.firstName, lastName = request.lastName, phoneNumber = request.phoneNumber, username = request.username, password = request.password ,role = request.role,\
                                           birthDate = request.birthDate, age = request.age, originCountry= request.originCountry, residenceCountry = request.residenceCountry,\
                                           residenceCity = request.residenceCity, address= request.address, person_repository=person_repository, user_repository=user_repository,\
                                           professional_repository=professional_repository)

def get_professionals(db: Session)->None:
    LOGGER.info("Listing all professionals")
    #professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    #professional_service.get_all_professionals(professional_repository=professional_repository)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    professional_list = person_service.get_all_professionals(person_repository=person_repository)
    
    if professional_list is None:
        LOGGER.info("Empty List in facade")
        return None
    else:
        LOGGER.info("List with data in facade")
        return professional_list