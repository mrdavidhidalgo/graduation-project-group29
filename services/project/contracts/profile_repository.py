import abc
from typing import Optional, List
from services.project.model import profile_model

class ProfileRepository(abc.ABC):
    
    def get_by_name(self, name: str)-> Optional[profile_model.Profile]:
        ... 
        
    def save(self, profile: profile_model.Profile)-> None:
        ...

    def get_profiles_by_project_id(self, project_id: str)->Optional[List[profile_model.Profile]]:
        ...