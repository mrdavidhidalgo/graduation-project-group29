import abc
from typing import Optional
from services.project.model import profile_model

class ProfileRepository(abc.ABC):
    
    def get_by_name(self, name: str)-> Optional[profile_model.Profile]:
        ... 
        
    def save(self, profile: profile_model.Profile)-> None:
        ...
