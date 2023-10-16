

from datetime import timedelta
import datetime

#from .contracts import user_repository
from services.professional.contracts import professional_repository
from services.user.contracts import user_repository
from services.professional.model import professional_model



from services import logs


LOGGER = logs.get_logger()

                
class ProfessionalAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "The person already exists as a professional"
        super().__init__(self.message)
        
class ProfessionalDoesNotExistError(Exception):
     def __init__(self, person_id: str, *args: object) -> None:
        self.message = f"The Professional with personID {person_id} does not exist"
        super().__init__(self.message)
    

def create_professional(birthDate: str, 
                        age: int,
                        originCountry: str, 
                        residenceCountry: str, 
                        residenceCity: str, 
                        address: str, 
                        person_id: str, 
                        professional_repository: professional_repository.ProfessionalRepository)-> None:
    
    LOGGER.info("Creating professional for person_id [%s]", person_id)
    
    persisted_professional = professional_repository.get_by_person_id(person_id = person_id)
    
    if persisted_professional is not None:
        raise ProfessionalAlreadyExistError()
    
    professional_repository.save(
        professional = professional_model.ProfessionalCreateModel(
            birthDate = birthDate,
            age = age,
            originCountry = originCountry,
            residenceCountry = residenceCountry,
            residenceCity = residenceCity,
            address = address,
            person_id = person_id )
        )
        
# Debe llegar el personID
def add_academic_info(academic_info :professional_model.ProfessionalAcademicInfo,  
                      professional_repository: professional_repository.ProfessionalRepository)->None:
    
    professional = professional_repository.get_by_person_id(person_id=academic_info.person_id)
    
    if professional is None:
        raise ProfessionalDoesNotExistError(person_id=academic_info.person_id)
    
    LOGGER.info("Creating academic professional info for professional [%s]", professional.id)
    
    professional_repository.add_academic_info(professional_id=professional.id, academic_info=academic_info)
    
    LOGGER.info("Academic professional info for professional [%s] was created", professional.id)