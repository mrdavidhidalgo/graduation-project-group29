

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

def create_company(request : CreateCompanyRequest, person_repository: person_repository.PersonRepository,\
user_repository: user_repository.UserRepository, company_repository: company_repository.CompanyRepository, employee_repository = employee_repository.EmployeeRepository)-> None:
    
    LOGGER.info("Creating Comapny with taxPayerId [%s] and name [%s]", request.taxpayerId, request.name)
    
    persisted_company = company_repository.get_by_taxpayerId(taxpayerId = request.taxpayerId)
    
    if persisted_company is not None:
        raise CompanyTaxprayerAlreadyExistError()
    
    person_request = person_service.CreateEmployeeRequest
    person_request.document = request.document
    person_request.documentType = request.documentType
    person_request.firstName = request.firstName
    person_request.lastName = request.lastName
    person_request.profile = request.profile
    person_request.position = request.position
    person_request.taxpayerId = request.taxpayerId
    
    company_repository.save(
        company = company_model.Company(
            taxpayerId = request.taxpayerId,
            name = request.name,
            country = request.country,
            city = request.city,
            years = request.years,
            address = request.address,
            phoneNumber = request.phoneNumber)
        )
    
    
    person_service.create_employee(person_request, person_repository, employee_repository)
        
    user_service.create_user(request.username, request.password, "COMPANY", request.document, user_repository)
    
    
def get_by_taxpayerId(company_repository: company_repository.CompanyRepository, taxpayerId: str)-> Optional[company_model.Company]:   
    LOGGER.info("Search for company by id")
    company =  company_repository.get_by_taxpayerId(taxpayerId)
    if list is None:
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