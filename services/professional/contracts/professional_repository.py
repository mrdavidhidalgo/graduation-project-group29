import abc
from services.professional.model import professional_model
from typing import List, Optional

class ProfessionalRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_person_id(self, person_id: str)-> Optional[professional_model.ProfessionalReadModel]:
        ...
        
    @abc.abstractmethod
    def save(self, professional: professional_model.ProfessionalCreateModel)-> None:
        ...
        
    @abc.abstractmethod
    def add_academic_info(self, professional_id : int, academic_info: professional_model.ProfessionalAcademicInfo)-> None:
        ...
        
    @abc.abstractmethod
    def add_laboral_info(self, professional_id : int, laboral_info: professional_model.ProfessionalLaboralInfo)-> None:
        ...
        
    @abc.abstractmethod
    def add_technology_info(self, professional_id : int, technology_info: professional_model.ProfessionalTechnologyInfo)-> None:
        ...
        
    @abc.abstractmethod
    def add_technical_role_info(self, professional_id : int, technical_role_info: professional_model.ProfessionalTechnicalRole)-> None:
        ...
    
    @abc.abstractmethod
    def delete_professional(self, person_id: int)-> Optional[int]:
        ...
        
    @abc.abstractmethod
    def search_for_candidates(self, role_filter: str, role: str, role_experience: str,\
     technologies: list, abilities: list , title_filter: str, title: str, title_experience: str)->Optional[List[professional_model.ProfessionalSearchResult]]:
        ...
        