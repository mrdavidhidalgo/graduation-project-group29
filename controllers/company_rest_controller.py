import datetime
from fastapi import APIRouter, HTTPException, Header, Response, status

from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Annotated, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal

from controllers import management_service_facade, commons
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
    request2 = management_service_facade.CreateCompanyRequest(document = request.document, document_type = request.documentType
    , first_name = request.firstName, last_name = request.lastName, username = request.username,
    password = request.password, taxpayer_id = request.taxpayerId, name = request.name, country = request.country,\
    city = request.city, years = request.years, address = request.address, phone_number = request.phoneNumber,\
    profile = request.profile, position = request.position)
        
    try:
        management_service_facade.create_company(request = request2, db = db)
        return {"msg": "Company has been created"}
    except (management_service_facade.CompanyTaxprayerAlreadyExistError, management_service_facade.UserNameAlreadyExistError,\
    management_service_facade.PersonDocumentAlreadyExistError) as e:
        raise HTTPException(status_code=400, detail=e.message)
        
@router.get("/companies")
async def get_companies(response: Response, db: Session = Depends(get_db)):
    companies_list = management_service_facade.get_companies(db = db)
    
    if companies_list is not None:
        data=[]
        for company in companies_list:
            data.append({'taxpayerId': str(company.taxpayer_id),'name': str(company.name)})
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No companies found")
        

@router.get("/companies/myself")
async def get_company_by_Id(token_data: commons.TokenData = Depends(commons.get_token_data), db: Session = Depends(get_db)):
    company = management_service_facade.get_company_by_person_id(person_id = token_data.person_id, db = db)
    
    if company is not None:
        data=[]
        co=str(company.country).split(".")
        dt=str(company.document_type).split(".")
        data.append({'document': str(company.document),'document_type': str(dt[1]),'first_name': str(company.first_name)
        ,'last_name': str(company.last_name),'username': str(company.username), 'password': str(company.password),'taxpayerId': str(company.taxpayer_id)
         ,'name': str(company.name),'country': str(co[1]), 'city': str(company.city), 'years': str(company.years),
         'address': str(company.address), 'phone_number': str(company.phone_number), 'profile': str(company.profile), 'position': str(company.position)})
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No companies found")
