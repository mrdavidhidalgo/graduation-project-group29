

from datetime import timedelta
import datetime

import jwt
from .contracts import user_repository
from services.user.contracts import user_repository
from services.user.model import user_model
import os
import random
from typing import Dict
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
    

def create_user(username: str, password: str, role: str, person: int, user_repository: user_repository.UserRepository)-> None:
    
    LOGGER.info("Creating user with username [%s]", username)
    
    persisted_user = user_repository.get_by_username(username = username)
    
    if persisted_user is not None:
        raise UserNameAlreadyExistError()
    
    user_repository.save(
        user = user_model.User(
            username = username,
            password = password,
            is_active = 'Y',
            role = role,
            person = int(person)
            )
        )
def login_user(username: str, password: str, user_repository: user_repository.UserRepository)-> None:
    
    LOGGER.info("Login user with username [%s]", username)

    persisted_user = user_repository.get_by_username(username = username)
    
    if persisted_user is None:
        raise UserLoginValidationError()
    
        
    if persisted_user.password == password:
        return create_access_token(data={"user": username,"role":persisted_user.role});
    
    raise UserLoginValidationError()
    
def myself(token: str)-> Dict[str,str]:
     
    return jwt.decode(token, _JWT_SECRET_KEY, algorithms=[_ALGORITHM])

    
    
def create_access_token(data: dict[str,str])->str:
    
    delta = timedelta(minutes=_JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES)
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, _JWT_SECRET_KEY, algorithm=_ALGORITHM)
    return encoded_jwt