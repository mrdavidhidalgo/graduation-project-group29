

from datetime import timedelta
import datetime
from typing import List, Optional

#from .contracts import user_repository
from services.person.contracts import person_repository
from services.user.contracts import user_repository
from services.company.contracts import company_repository
from services.employee.contracts import employee_repository
from services.person.model import person_model
from services.user.model import user_model
from services.company.model import company_model
from services.user import user_service
from services.employee import employee_service
from services.company import company_service
from services.person import person_service
from pydantic import BaseModel


import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class CompanyTaxprayerAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Tax PrayerID  is already used"
        super().__init__(self.message)
        
class CreateCompanyRequest(BaseModel):
    document: str
    document_type: str
    first_name: str
    last_name: str
    username: str
    password: str
    taxpayer_id: str
    name: str
    country: str
    city: str
    years: str
    address: str
    phone_number: str
    profile: str
    position: str

def create_company(request : CreateCompanyRequest, person_repository: person_repository.PersonRepository,\
user_repository: user_repository.UserRepository, company_repository: company_repository.CompanyRepository, employee_repository = employee_repository.EmployeeRepository)-> None:
    
    LOGGER.info("Creating Comapny with taxPayerId [%s] and name [%s]", request.taxpayer_id, request.name)
    
    persisted_company = company_repository.get_by_taxpayerId(taxpayer_id = request.taxpayer_id)
    
    if persisted_company is not None:
        raise CompanyTaxprayerAlreadyExistError()
    
    person_request = person_service.CreateEmployeeRequest
    person_request.document = request.document
    person_request.document_type = request.document_type
    person_request.first_name = request.first_name
    person_request.last_name = request.last_name
    person_request.profile = request.profile
    person_request.position = request.position
    person_request.taxpayer_id = request.taxpayer_id
    
    company_repository.save(
        company = company_model.Company(
            taxpayer_id = request.taxpayer_id,
            name = request.name,
            country = request.country,
            city = request.city,
            years = request.years,
            address = request.address,
            phone_number = request.phone_number)
        )
    
    try:
        person_service.create_employee(person_request, person_repository, employee_repository)
    except:
        LOGGER.info("Haciendo Rollback de Empresa")
        company_repository.delete_company(request.taxpayer_id)
        raise
        
    try:    
        user_service.create_user(request.username, request.password, "COMPANY", request.document, user_repository)
    except:
        LOGGER.info("Haciendo Rollback desde Usuario")
        company_repository.delete_company(request.taxpayer_id)
        employee_repository.delete_employee(request.document)
        person_repository.delete_person(request.document)
        raise user_service.UserNameAlreadyExistError()
    
    
def get_by_taxpayerId(company_repository: company_repository.CompanyRepository, taxpayer_id: str)-> Optional[company_model.Company]:   
    LOGGER.info("Search for company by id")
    company =  company_repository.get_by_taxpayerId(taxpayer_id)
    if company is None:
        LOGGER.info("Company not exists")
        return None
    else:
        LOGGER.info("Company exists in service")
        return company
        
def get_all(company_repository: company_repository.CompanyRepository)->List[company_model.Company]:
    LOGGER.info("Search for companies in service")
    list =  company_repository.get_all()
    if list is None:
        LOGGER.info("Empty List company in service")
        return None
    else:
        LOGGER.info("Company List with data in service")
        return list