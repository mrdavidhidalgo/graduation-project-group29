
from sqlalchemy.orm import Session
from services.user import user_service
from daos import db_user_repository
from pydantic import BaseModel

class LoginResponse(BaseModel):
    token: str
    username: str
    
UserLoginValidationError = user_service.UserLoginValidationError

UserLoginError = user_service.UserLoginError

UserNameAlreadyExistError = user_service.UserNameAlreadyExistError

LOGGER = user_service.LOGGER
    
class LoginRequest(BaseModel):
    username: str
    password: str
    
class CreateUserRequest(BaseModel):
    username: str
    password: str
    name: str

def login(login_request: LoginRequest, db: Session)->LoginResponse:
    
    user_repository = db_user_repository.DBUserRepository(db = db)
    
    token = user_service.login_user(user_repository=user_repository, username=login_request.username, password=login_request.password)
    
    return LoginResponse(token = token, username=login_request.username) 

def create_user(request: CreateUserRequest, db: Session)->None:
    
    user_repository = db_user_repository.DBUserRepository(db = db)
    
    user_service.create_user(user_repository=user_repository, username=request.username, password=request.password, name = request.name)
    