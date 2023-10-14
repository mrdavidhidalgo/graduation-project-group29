from typing import Optional
from .db_model import db_model as models

from services.professional.contracts import professional_repository

from sqlalchemy.orm import Session

from services.professional.model import professional_model

class DBProfessionalRepository(professional_repository.ProfessionalRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_person_id(self, person_id: int)-> Optional[professional_model.Professional]:
        professional = self.db.query(models.Professional).filter(models.Professional.person_id == person_id).first()
       
        return None if professional is None else professional_model.Professional(birthDate = professional.birthDate , age=professional.age,\
        originCountry= professional.originCountry, residenceCountry = professional.residenceCountry, residenceCity = professional.residenceCity,\
        address = professional.address, person_id = person_id )
        
    def save(self, professional: professional_model.Professional)-> None:
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
        
        