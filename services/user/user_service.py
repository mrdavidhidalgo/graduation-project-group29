

from datetime import timedelta
import datetime
import math     
import jwt
from .contracts import user_repository
from services.user.contracts import user_repository
from services.user.model import user_model
import os
import random
from typing import Dict,Tuple
from services import logs

# Configura un secreto para firmar los tokens JWT
_JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "DATA")
_JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES", 15)
_ALGORITHM = "HS256"


LOGGER = logs.get_logger()

class UserLoginError(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__("Error trying to login user")
        
class UserLoginValidationError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Invalid password for user"
        super().__init__(self.message)
        
class UserNameAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Username to use is already used"
        super().__init__(self.message)
        
class UserNameDoesNotExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Username does not exist"
        super().__init__(self.message)
    

def create_user(username: str, password: str, role: str, person_id: str, user_repository: user_repository.UserRepository)-> None:
    
    LOGGER.info("Creating user with username [%s] and role [%s]", username, role)
    
    persisted_user = user_repository.get_by_username(username = username)
    
    if persisted_user is not None:
        raise UserNameAlreadyExistError()
    
    if role == "COMPANY":
       role_aux = user_model.UserRole.CLIENT 
    elif role == "RECRUITER":
       role_aux = user_model.UserRole.RECRUITER 
    else:
       role_aux = user_model.UserRole.CANDIDATE
    
    
    user_repository.save(
        user = user_model.User(
            username = username,
            password = password,
            is_active = True,
            role = role_aux,
            person_id = person_id
            )
        )
        
def login_user(username: str, password: str, user_repository: user_repository.UserRepository)-> str:
    
    LOGGER.info("Login user with username [%s]", username)

    persisted_user = user_repository.get_by_username(username = username)
    
    if persisted_user is None:
        raise UserLoginValidationError()
    
        
    if persisted_user.password == password:
        return create_access_token(data={"user": username,
                                         "role":persisted_user.role.name,"person_id":persisted_user.person_id})[0];
    
    raise UserLoginValidationError()

def get_user_by_username(username: str, user_repository: user_repository.UserRepository)-> None:
    
    LOGGER.info("Getting user with username [%s]", username)

    persisted_user = user_repository.get_by_username(username = username)
    
    
    
    if persisted_user is None:
        raise UserLoginValidationError()
    
        
    if persisted_user.password == password:
        return create_access_token(data={"user": username})[0];
    
    raise UserLoginValidationError()
    
def myself(token: str)-> Tuple[str,Dict[str,str]]:
     
    map = jwt.decode(token, _JWT_SECRET_KEY, algorithms=[_ALGORITHM])
    
    return create_access_token(map)


    
    
def create_access_token(data: dict[str,str])->Tuple[str,Dict[str,str]]:
    
    delta = timedelta(minutes=_JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES)
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + delta
    to_encode.update({"exp": math.floor(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, _JWT_SECRET_KEY, algorithm=_ALGORITHM)
    return encoded_jwt,to_encode