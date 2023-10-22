import datetime
from fastapi import APIRouter, HTTPException, Header, Response, status

from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Annotated, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal

from controllers import management_service_facade
from services import logs
LOGGER = logs.get_logger()

router = APIRouter()

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

    
# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/companies")
async def create_company(request: CreateCompanyRequest, db: Session = Depends(get_db)):
    #LOGGER.info("Peticion [%s] - [%s]", str(request.document), str(request.documentType))
    request2 = management_service_facade.CreateCompanyRequest(document = request.document, documentType = request.documentType
    , firstName = request.firstName, lastName = request.lastName, username = request.username,
    password = request.password, taxpayerId = request.taxpayerId, name = request.name, country = request.country,\
    city = request.city, years = request.years, address = request.address, phoneNumber = request.phoneNumber,\
    profile = request.profile, position = request.position)
        
    try:
        management_service_facade.create_company(request = request2, db = db)
        return {"msg": "Company has been created"}
    except (management_service_facade.CompanyTaxprayerAlreadyExistError, management_service_facade.UserNameAlreadyExistError) as e:
        raise HTTPException(status_code=400, detail=e.message)
        
@router.get("/companies")
async def get_companies(response: Response, db: Session = Depends(get_db)):
    companies_list = management_service_facade.get_companies(db = db)
    
    if companies_list is not None:
        data=[]
        for company in companies_list:
            data.append({'id': str(company.id),'taxpayerId': str(company.taxpayerId),'name': str(company.name)})
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No companies found")