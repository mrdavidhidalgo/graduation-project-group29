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
       
        return None if professional is None else professional_model.ProfessionalReadModel(id = professional.id, birthDate = professional.birthDate , age=professional.age,\
        originCountry= professional.originCountry, residenceCountry = professional.residenceCountry, residenceCity = professional.residenceCity,\
        address = professional.address, person_id = person_id )
        
    def save(self, professional: professional_model.ProfessionalCreateModel)-> None:
        new_professional = models.Professional(
            birthDate = professional.birthDate,
            age = professional.age,
            originCountry = professional.originCountry,
            residenceCountry = professional.residenceCountry,
            residenceCity = professional.residenceCity,
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
        
        