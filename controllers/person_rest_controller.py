from fastapi import APIRouter, HTTPException, Header, Response, status

from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal

from controllers import management_service_facade
from services import logs
LOGGER = logs.get_logger()

router = APIRouter()
    
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

    
# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.post("/candidate")
async def create_professional(request: CreateProfessionalRequest, db: Session = Depends(get_db)):
    request = management_service_facade.CreateProfessionalRequest(document = request.document, documentType = request.documentType,
                                           firstName=request.firstName, lastName = request.lastName, phoneNumber = request.phoneNumber, username = request.username,\
                                           password = request.password, role = request.role,  birthDate = request.birthDate, age = request.age, originCountry= request.originCountry,\
                                           residenceCountry = request.residenceCountry, residenceCity = request.residenceCity, address= request.address)
    
    try:
        management_service_facade.create_professional(request = request, db = db)
        return {"msg": "Person han been created"}
    except management_service_facade.PersonDocumentAlreadyExistError as e:
        raise HTTPException(status_code=400, detail=e.message)
        
@router.get("/candidates")
async def get_professionals(response: Response, db: Session = Depends(get_db)):
    professional_list = management_service_facade.get_professionals(db = db)
    
    if professional_list is not None:
        data=[]
        for professional in professional_list:
            data.append({'document': str(professional.document), 'documentType': str(professional.documentType)})
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No professionals found")