from typing import Optional, List
from .db_model import db_model as models

from services.technology.contracts import technology_repository

from sqlalchemy.orm import Session

from services.technology.model import technology_model
from services import logs
LOGGER = logs.get_logger()

class DBTechnologyRepository(technology_repository.TechnologyRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
    
    def get_all(self)->Optional[List[technology_model.TechnologyRead]]:
        
        technologies = self.db.query(models.Technology).all()
        if len(technologies) ==0:
            LOGGER.info("There are not technology records")
            None
        else:
            LOGGER.info("Sending technology list")
            return [technology_model.TechnologyRead(id = technology.id, technology_name=technology.technology_name,\
            details = technology.details, category = technology.category)   for technology in technologies]
                
    def save(self, technology: technology_model.TechnologyCreate)-> None:
        new_technology = models.Technology(
            technology_name = technology.project_name,
            details = technology.details,
            category = technology.category
        )
        
        self.db.add(new_technology)
        self.db.commit()
        

    def get_by_name(self, technology_name: str)->Optional[List[technology_model.TechnologyRead]]:   
        technology = self.db.query(models.Technology).filter(models.Technology.technology_name == technology_name).first()
       
        return None if technology is None else technology_model.TechnologyRead(id = technology.id, project_name=technology.project_name,\
            details = technology.details, category = technology.category)

    """def delete_technology(self, technology_id: int)-> Optional[int]:
        technology = self.db.query(models.Technology).filter(models.Technology.id == technology_id).delete()
        self.db.commit()
        return technology"""
 
  