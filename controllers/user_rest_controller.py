from fastapi import APIRouter, HTTPException, Header

from fastapi import Depends
from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal

from controllers import management_service_facade

router = APIRouter()
    
class LoginResponse(BaseModel):
    id_request: str
    autenticated: bool
    
class LoginRequest(BaseModel):
    username: str
    password: str
    
class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str
    person: int

# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.post("/user/login")
async def login(login_request: LoginRequest, db: Session = Depends(get_db),request_id: Annotated[str | None, Header(convert_underscores=False)] = None):
    
    request = management_service_facade.LoginRequest(username = login_request.username, 
                                           password=login_request.password)
    try: 
        login_response = management_service_facade.login(login_request=request, db = db)
    except management_service_facade.UserLoginValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except management_service_facade.UserLoginError as e:
        management_service_facade.LOGGER.error("Unexpected error for request: %s", request_id)
        raise e
    
    return {"username":login_response.username, "token": login_response.token}

@router.post("/user")
async def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    request = management_service_facade.CreateUserRequest(username = request.username, 
                                           password=request.password, role=request.role, person = request.person)
    
    try:
        management_service_facade.create_user(request = request, db = db)
        return {"msg": "User han beed created"}
    except management_service_facade.UserNameAlreadyExistError as e:
        raise HTTPException(status_code=400, detail=e.message)