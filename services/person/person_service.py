

from datetime import timedelta
import datetime

#from .contracts import user_repository
from services.person.contracts import person_repository
from services.user.contracts import user_repository
from services.professional.contracts import professional_repository
from services.person.model import person_model
from services.user.model import user_model
from services.user import user_service
from services.professional import professional_service


import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class PersonDocumentAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Document number is already used"
        super().__init__(self.message)
    

def create_professional(document: int, documentType: str, firstName: str, lastName: str, phoneNumber: str, username: str, password: str, role: str,\
birthDate: str, age: int, originCountry: str, residenceCountry: str, residenceCity: str, address: str, person_repository: person_repository.PersonRepository,\
user_repository: user_repository.UserRepository, professional_repository: professional_repository.ProfessionalRepository)-> None:
    
    LOGGER.info("Creating person with document [%d] and documentType [%s]", document, documentType)
    
    persisted_person = person_repository.get_by_document(document = document)
    
    if persisted_person is not None:
        raise PersonDocumentAlreadyExistError()
    
    person_repository.save(
        person = person_model.Person(
            document = document,
            documentType = documentType,
            firstName = firstName,
            lastName = lastName,
            phoneNumber = phoneNumber)
        )
        
    user_service.create_user(username, password,  role, document, user_repository)
    
    professional_service.create_professional(birthDate, age, originCountry, residenceCountry, residenceCity, address, document, professional_repository)
    
    
def get_all_professionals(person_repository: person_repository.PersonRepository):
    LOGGER.info("Search professionals in service")
    professional_list =  person_repository.get_all_professionals()
    if professional_list is None:
        LOGGER.info("Empty List in service")
        return None
    else:
        LOGGER.info("List with data in service")
        return professional_list