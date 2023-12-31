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
                project_id=profile.project_id
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
                project_id=profile.project_id
        )
        
        self.db.add(new_profile)
        self.db.commit()

    def get_profiles_by_project_id(self, project_id: str)->Optional[List[profile_model.Profile]]:
        profiles = self.db.query(models.Profile).filter(models.Profile.project_id == project_id).all()
        if len(profiles) ==0:
            LOGGER.info("There are not profiles records associated to project [%s]", project_id)
            None
        else:
            LOGGER.info("Sending profile list [%s]", project_id)
            return [profile_model.Profile( name=profile.name, description = profile.description,\
             role= profile.role, experience_in_years = profile.experience_in_years,\
            technology = profile.technology, category = profile.category, title = profile.title,\
             project_id = str(project_id))   for profile in profiles]
    
 