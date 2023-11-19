

from datetime import timedelta
import datetime
from typing import List, Optional
#from .contracts import user_repository
from services.professional.contracts import professional_repository
from services.user.contracts import user_repository
from services.professional.model import professional_model
from services.commons import base
from pydantic import BaseModel


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

class ProfessionalSearchError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "There are not professionals associated"
        super().__init__(self.message)

    
class CandidateSearchRequest(BaseModel):
    role_filter: str
    role: str
    role_experience: str
    technologies: list = []
    abilities: list = []
    title_filter: str
    title: str
    title_experience: str
    
def create_professional(birth_date: str, 
                        age: int,
                        origin_country: base.Country, 
                        residence_country: base.Country, 
                        residence_city: str, 
                        address: str, 
                        person_id: str, 
                        professional_repository: professional_repository.ProfessionalRepository)-> None:
    
    LOGGER.info("Creating professional for person_id [%s]", person_id)
    
    persisted_professional = professional_repository.get_by_person_id(person_id = person_id)
    
    if persisted_professional is not None:
        raise ProfessionalAlreadyExistError()
    
    professional_repository.save(
        professional = professional_model.ProfessionalCreateModel(
            birth_date = birth_date,
            age = age,
            origin_country = origin_country,
            residence_country = residence_country,
            residence_city = residence_city,
            address = address,
            person_id = person_id )
        )
        
def add_academic_info(academic_info :professional_model.ProfessionalAcademicInfo,  
                      professional_repository: professional_repository.ProfessionalRepository)->None:
    
    professional = professional_repository.get_by_person_id(person_id=academic_info.person_id)
    
    if professional is None:
        raise ProfessionalDoesNotExistError(person_id=academic_info.person_id)
    
    LOGGER.info("Creating academic info for professional [%s]", professional.id)
    
    professional_repository.add_academic_info(professional_id=professional.id, academic_info=academic_info)
    
    LOGGER.info("Academic info for professional [%s] was created", professional.id)
    

def add_laboral_info(laboral_info :professional_model.ProfessionalLaboralInfo,  
                      professional_repository: professional_repository.ProfessionalRepository)->None:
    
    professional = professional_repository.get_by_person_id(person_id=laboral_info.person_id)
    
    if professional is None:
        raise ProfessionalDoesNotExistError(person_id=laboral_info.person_id)
    
    LOGGER.info("Creating laboral info for professional [%s]", professional.id)
    
    professional_repository.add_laboral_info(professional_id=professional.id, laboral_info=laboral_info)
    
    LOGGER.info("Laboral info for professional [%s] was created", professional.id)
    
def add_technical_role(technical_role :professional_model.ProfessionalTechnicalRole,  
                      professional_repository: professional_repository.ProfessionalRepository)->None:
    
    professional = professional_repository.get_by_person_id(person_id=technical_role.person_id)
    
    if professional is None:
        raise ProfessionalDoesNotExistError(person_id=technical_role.person_id)
    
    LOGGER.info("Creating technical role info for professional [%s]", professional.id)
    
    professional_repository.add_technical_role_info(professional_id=professional.id, technical_role_info=technical_role)
    
    LOGGER.info("Technical role info for professional [%s] was created", professional.id)
    
def add_technology_info(technology_info :professional_model.ProfessionalTechnologyInfo,  
                      professional_repository: professional_repository.ProfessionalRepository)->None:
    
    professional = professional_repository.get_by_person_id(person_id=technology_info.person_id)
    
    if professional is None:
        raise ProfessionalDoesNotExistError(person_id=technology_info.person_id)
    
    LOGGER.info("Creating technology info for professional [%s]", professional.id)
    
    professional_repository.add_technology_info(professional_id=professional.id, technology_info=technology_info)
    
    LOGGER.info("Technology info for professional [%s] was created", professional.id)
    
def search_for_candidates(request: CandidateSearchRequest, professional_repository: professional_repository.ProfessionalRepository)->Optional[List[professional_model.ProfessionalSearchResult]]:
    LOGGER.info("Search for candidates with filters")
    
    candidates = professional_repository.search_for_candidates(role_filter= request.role_filter, role= request.role,\
     role_experience=request.role_experience ,technologies_list=request.technologies,\
     abilities_list= request.abilities, title_filter=request.title_filter, title=request.title, title_experience=request.title_experience)
    if candidates is None:
        LOGGER.info("NO candidates found on service")
        return None
    else:
        LOGGER.info("Candidates list exists in service")
        return candidates
    
def get_by_person_id(person_id: str, professional_repository : professional_repository.ProfessionalRepository)->professional_model.ProfessionalReadModel:
    
    professional = professional_repository.get_by_person_id(person_id=person_id)
    if professional is None:
        raise ProfessionalDoesNotExistError(person_id=person_id)
    
    return professional 

def get_full_info(person_id: str, professional_repository : professional_repository.ProfessionalRepository)->professional_model.ProfessionalFullInfo:
    
    return professional_repository.get_full_info(professional_id=person_id)
    
    