

from datetime import timedelta
import datetime
from typing import List

#from .contracts import user_repository
from services.person.contracts import person_repository
from services.user.contracts import user_repository
from services.professional.contracts import professional_repository
from services.person.model import person_model
from services.employee.contracts import employee_repository
from services.user.model import user_model
from services.user import user_service
from services.employee import employee_service
from services.professional import professional_service
from pydantic import BaseModel
from services.commons import base


import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class PersonDocumentAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Document number is already used"
        super().__init__(self.message)
        
class CreateCandidateRequest(BaseModel):
    document: str
    documentType: base.DocumentType
    firstName: str
    lastName: str
    phoneNumber: str
    username: str
    password: str
    birthDate: str
    age: int
    originCountry: base.Country
    residenceCountry: base.Country
    residenceCity: str
    address: str    

class CreatePersonRequest(BaseModel):
    document: str
    document_type: str
    first_name: str
    last_name: str
    phone_number: str 

class CreateEmployeeRequest(BaseModel):
    document: str
    documentType: str
    firstName: str
    lastName: str
    profile: str
    position: str
    taxpayerId: str

def create_person(request : CreatePersonRequest, person_repository: person_repository.PersonRepository)-> None:
    
    LOGGER.info("Creating person with document [%s] and documentType [%s]", request.document, request.document_type)
    
    persisted_person = person_repository.get_by_document(document = request.document)
    
    if persisted_person is not None:
        raise PersonDocumentAlreadyExistError()
    
    person_repository.save(
        person = person_model.Person(
            document = request.document,
            document_type = request.document_type,
            first_name = request.first_name,
            last_name = request.last_name,
            phone_number = request.phone_number)
        )
    
def create_candidate(request : CreateCandidateRequest, person_repository: person_repository.PersonRepository,\
user_repository: user_repository.UserRepository, professional_repository: professional_repository.ProfessionalRepository)-> None:
    
    LOGGER.info("Creating candidate with document [%s] and documentType [%s]", request.document, request.documentType)
    
    persisted_person = person_repository.get_by_document(document = request.document)
    
    if persisted_person is not None:
        raise PersonDocumentAlreadyExistError()
    
    person_repository.save(
        person = person_model.Person(
            document = request.document,
            document_type = request.documentType,
            first_name = request.firstName,
            last_name = request.lastName,
            phone_number = request.phoneNumber)
        )
        
    user_service.create_user(request.username, request.password, "CANDIDATE", request.document, user_repository)
    
    professional_service.create_professional(request.birthDate, 
                                             request.age, 
                                             request.originCountry, 
                                             request.residenceCountry, 
                                             request.residenceCity, 
                                             request.address, 
                                             request.document, 
                                             professional_repository)
    
def create_employee(request : CreateEmployeeRequest, person_repository: person_repository.PersonRepository, employee_repository: employee_repository.EmployeeRepository)-> None:
    
    LOGGER.info("Creating Employee with document [%s] and documentType [%s]", request.document, request.documentType)
   
    persisted_person = person_repository.get_by_document(document = request.document)
    
    if persisted_person is not None:
        raise PersonDocumentAlreadyExistError()
    
    person_repository.save(
        person = person_model.Person(
            document = request.document,
            document_type = request.documentType,
            first_name = request.firstName,
            last_name = request.lastName,
            phone_number="")
        )
    
    employee_service.create_employee(request.profile, request.position, request.taxpayerId, request.document, employee_repository)
   
def get_all(person_repository: person_repository.PersonRepository)->List[person_model.Person]:
    LOGGER.info("Search professionals in service")
    list =  person_repository.get_all()
    if list is None:
        LOGGER.info("Empty List in service")
        return None
    else:
        LOGGER.info("List with data in service")
        return list