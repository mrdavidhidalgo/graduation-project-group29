

from datetime import timedelta
import datetime

import jwt
from .contracts import user_repository
from services.user.contracts import user_repository
import os
import random

from services import logs

# Configura un secreto para firmar los tokens JWT
_JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "DATA")
_JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES", 1)
_ALGORITHM = "HS256"
_RANDOM_ERROR = os.getenv('RANDOM_ERROR', False)
_PROBABILITY_ERROR = os.getenv('PROBABILITY_ERROR', 100)

LOGGER = logs.get_logger()

class UserLoginError(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__("Error trying to login user")
        
class UserLoginValidationError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Invalid password for user"
        super().__init__(self.message)
    

def login_user(username: str, password: str, user_repository: user_repository.UserRepository)-> None:
    
    LOGGER.info("Login user with username [%s]", username)
    
    persisted_user = user_repository.get_by_username(username = username)
    
    if persisted_user is None:
        raise UserLoginValidationError()
    
    validate_error_generation()
        
    if persisted_user.password == password:
        return create_access_token(data={"user": username});
    
    raise UserLoginValidationError()
    
    
def validate_error_generation()->None:
    
    if not _RANDOM_ERROR:
        return
    
    number = random.randint(1,100)
    if number < _PROBABILITY_ERROR:
        raise UserLoginError()
    
def create_access_token(data: dict[str,str])->str:
    
    delta = timedelta(minutes=_JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES)
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, _JWT_SECRET_KEY, algorithm=_ALGORITHM)
    return encoded_jwt