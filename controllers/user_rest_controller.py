from fastapi import APIRouter

from fastapi import Depends

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal

from controllers import management_service_facade

router = APIRouter()
    
class LoginResponse(BaseModel):
    id_request: str
    autenticated: bool
    
class LoginRequest(BaseModel):
    id_request: str
    username: str
    password: str

# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.post("/user/login", status_code=201)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    
    request = management_service_facade.LoginRequest(id_request=login_request.id_request, 
                                           username = login_request.username, 
                                           password=login_request.password)
    
    login_response = management_service_facade.login(login=request, db = db)
    
    return {"username":login_response.username, "token": login_response.token}