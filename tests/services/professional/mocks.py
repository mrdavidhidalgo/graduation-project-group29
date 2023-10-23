from typing import Optional
from services.commons import base
from services.professional.contracts import professional_repository
from services.professional.model import professional_model

class FakeProfesionalRepository(professional_repository.ProfessionalRepository):
    
    def __init__(self, person_id: Optional[str]= None) -> None:
        super().__init__()
        self.person_id = person_id
    
    def get_by_person_id(self, person_id: str)-> Optional[professional_model.ProfessionalReadModel]:
        return None if self.person_id is None else professional_model.ProfessionalReadModel(id=1, 
                                                                                            birthDate="2023-05-01", 
                                                                                            age=35, 
                                                                                            originCountry=base.Country.Colombia, 
                                                                                            residenceCountry=base.Country.Colombia,
                                                                                            residenceCity="Santa Marta",
                                                                                            address="Calle 125", 
                                                                                            person_id=person_id)
        
    def save(self, professional: professional_model.ProfessionalCreateModel)-> None:
        ...
        
    def add_academic_info(self, professional_id : int, academic_info: professional_model.ProfessionalAcademicInfo)-> None:
        ...
        
    def add_laboral_info(self, professional_id : int, laboral_info: professional_model.ProfessionalLaboralInfo)-> None:
        ...
        
    def add_technology_info(self, professional_id : int, technology_info: professional_model.ProfessionalTechnologyInfo)-> None:
        ...
        
    def add_technical_role_info(self, professional_id : int, technical_role_info: professional_model.ProfessionalTechnicalRole)-> None:
        ...
        