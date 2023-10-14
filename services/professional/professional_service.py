

from datetime import timedelta
import datetime

#from .contracts import user_repository
from services.professional.contracts import professional_repository
from services.professional.model import professional_model


import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class ProfessionalAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "The person already exists as a professional"
        super().__init__(self.message)
    

def create_professional(birthDate: str, age: int,originCountry: str, residenceCountry: str, residenceCity: str, address: str, person_id: int, professional_repository: professional_repository.ProfessionalRepository)-> None:
    
    LOGGER.info("Creating professional with person_id [%d]", person_id)
    
    persisted_professional = professional_repository.get_by_person_id(person_id = person_id)
    
    if persisted_professional is not None:
        raise ProfessionalAlreadyExistError()
    
    professional_repository.save(
        professional = professional_model.Professional(
            birthDate = birthDate,
            age = age,
            originCountry = originCountry,
            residenceCountry = residenceCountry,
            residenceCity = residenceCity,
            address = address,
            person_id = person_id )
        )
        
def get_all_professionals(professional_repository: professional_repository.ProfessionalRepository):
    professionals_list =  professional_repository.get_all_professionals()
    if professionals_list is None:
        LOGGER.info("Returning professional data NO data")
        return None
    else:
        LOGGER.info("Returning professional data from service")
        return professionals_list
