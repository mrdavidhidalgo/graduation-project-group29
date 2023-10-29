from typing import Optional
from .db_model import db_model as models

from services.professional.contracts import professional_repository

from sqlalchemy.orm import Session

from services.professional.model import professional_model

class DBProfessionalRepository(professional_repository.ProfessionalRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_person_id(self, person_id: str)-> Optional[professional_model.ProfessionalReadModel]:
        professional = self.db.query(models.Professional).filter(models.Professional.person_id == person_id).first()
       
        return None if professional is None else professional_model.ProfessionalReadModel(id = professional.id, birth_date = professional.birth_date , age=professional.age,\
        origin_country= professional.origin_country, residence_country = professional.residence_country, residence_city = professional.residence_city,\
        address = professional.address, person_id = person_id )
        
    def save(self, professional: professional_model.ProfessionalCreateModel)-> None:
        new_professional = models.Professional(
            birth_date = professional.birth_date,
            age = professional.age,
            origin_country = professional.origin_country,
            residence_country = professional.residence_country,
            residence_city = professional.residence_city,
            address = professional.address,
            person_id = professional.person_id
        )
        
        self.db.add(new_professional)
        self.db.commit()
        
    def add_academic_info(self, professional_id: int, academic_info: professional_model.ProfessionalAcademicInfo)-> None:
        academic_info = models.ProfessionalAcademicInfo(
            professional_id = professional_id,
            title = academic_info.title,
            institution = academic_info.institution,
            country = academic_info.country,
            start_date = academic_info.start_date,
            end_date = academic_info.end_date,
            description = academic_info.description
        )
        
        self.db.add(academic_info)
        self.db.commit()
        
    def add_laboral_info(self, professional_id: int, laboral_info: professional_model.ProfessionalLaboralInfo)-> None:
        laboral_info = models.ProfessionalLaboralInfo(
            professional_id = professional_id,
            position = laboral_info.position,
            company_name = laboral_info.company_name,
            company_country = laboral_info.company_country,
            company_address = laboral_info.company_address,
            company_phone = laboral_info.company_phone,
            start_date = laboral_info.start_date,
            end_date = laboral_info.end_date,
            description = laboral_info.description
        )
        
        self.db.add(laboral_info)
        self.db.commit()
        
    def add_technical_role_info(self, professional_id: int, technical_role_info: professional_model.ProfessionalTechnicalRole)-> None:
        technical_role = models.ProfessionalTechnicalRoleInfo(
            professional_id = professional_id,
            role = technical_role_info.role,
            experience_years = technical_role_info.experience_years,
            description = technical_role_info.description

        )
        
        self.db.add(technical_role)
        self.db.commit()
        
    def add_technology_info(self, professional_id: int, technology_info: professional_model.ProfessionalTechnologyInfo)-> None:
        technology_info = models.ProfessionalTechnologyInfo(
            professional_id = professional_id,
            name = technology_info.name,
            level = technology_info.level,
            experience_years = technology_info.experience_years,
            description = technology_info.description

        )
        
        self.db.add(technology_info)
        self.db.commit()
        
    def delete_professional(self, person_id: int)-> Optional[int]:
        professional = self.db.query(models.Professional).filter(models.Professional.person_id == person_id).delete()
        self.db.commit()
        return professional 
  