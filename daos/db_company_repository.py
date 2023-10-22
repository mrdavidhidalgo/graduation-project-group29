from typing import Optional, List
from .db_model import db_model as models

from services.company.contracts import company_repository

from sqlalchemy.orm import Session

from services.company.model import company_model
from services import logs
LOGGER = logs.get_logger()

class DBCompanyRepository(company_repository.CompanyRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_taxpayerId(self, taxpayerId: str)-> Optional[company_model.Company]:
        company = self.db.query(models.Company).filter(models.Company.taxpayerId == taxpayerId).first()
       
        return None if company is None else company_model.Company(id = company.id, taxpayerId=taxpayerId, name = company.name,\
        country= company.country, city = company.city, years=str(company.years), address = company.address,\
        phoneNumber = company.phoneNumber)
    
    def get_all(self)-> Optional[List[company_model.Company]]:
        
        companies = self.db.query(models.Company).all()
        if len(companies) ==0:
            LOGGER.info("There are not company records")
            None
        else:
            LOGGER.info("Sending company list")
            return [company_model.Company(id = company.id , taxpayerId=company.taxpayerId, name=company.name,
             country = company.country, city = company.city, years= company.years, address = company.phoneNumber ) 
            for company in companies]
                
    def save(self, company: company_model.Company)-> None:
        new_company = models.Company(
            taxpayerId = company.taxpayerId,
            name = company.name,
            country = company.country,
            city = company.city,
            years = company.years,
            address = company.address,
            phoneNumber = company.phoneNumber
        )
        
        self.db.add(new_company)
        self.db.commit()

        
        