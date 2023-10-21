

from datetime import timedelta
import datetime
from typing import List

#from .contracts import user_repository
from services.person.contracts import person_repository
from services.user.contracts import user_repository
from services.professional.contracts import professional_repository
from services.person.model import person_model
from services.user.model import user_model
from services.user import user_service
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
    document_type: base.DocumentType
    first_name: str
    last_name: str
    phone_number: str
    username: str
    password: str
    birth_date: str
    age: int
    origin_country: base.Country
    residence_country: base.Country
    residence_city: str
    address: str    

def create_candidate(request : CreateCandidateRequest, person_repository: person_repository.PersonRepository,\
user_repository: user_repository.UserRepository, professional_repository: professional_repository.ProfessionalRepository)-> None:
    
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
        
    user_service.create_candidate_user(request.username, request.password, request.document, user_repository)
    
    professional_service.create_professional(request.birth_date, 
                                             request.age, 
                                             request.origin_country, 
                                             request.residence_country, 
                                             request.residence_city, 
                                             request.address, 
                                             request.document, 
                                             professional_repository)
    
    
def get_all(person_repository: person_repository.PersonRepository)->List[person_model.Person]:
    LOGGER.info("Search professionals in service")
    list =  person_repository.get_all()
    if list is None:
        LOGGER.info("Empty List in service")
        return None
    else:
        LOGGER.info("List with data in service")
        return list