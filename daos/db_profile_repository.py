from pydoc import describe
from typing import Optional, List
from .db_model import db_model as models

from services.project.contracts import profile_repository

from sqlalchemy.orm import Session

from services.project.model import profile_model
from services import logs
LOGGER = logs.get_logger()

class DBProfileRepository(profile_repository.ProfileRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_name(self, name: str)-> Optional[profile_model.Profile]:
        profile = self.db.query(models.Profile).filter(models.Profile.name == name).first()
       
        return None if profile is None else profile_model.Profile(  
                name = profile.name,
                description=profile.description,
                experience_in_years=profile.experience_in_years,
                role=profile.role,
                technology=profile.technology,
                category=profile.category,
                title=profile.title,
        )
          
    def save(self, profile: profile_model.Profile)-> None:
        new_profile = models.Profile(
                name = profile.name,
                description=profile.description,
                experience_in_years=profile.experience_in_years,
                role=profile.role,
                technology=profile.technology,
                category=profile.category,
                title=profile.title,
        )
        
        self.db.add(new_profile)
        self.db.commit()

