from services import logs
from services.project.contracts import profile_repository
from services.project.model import profile_model
from pydantic import BaseModel,Field

LOGGER = logs.get_logger()

class ProfileNameAlreadyExistError(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__("Error trying to create profile")
        
class CreateProfileRequest(BaseModel):
    name : str = Field(min_length=6,max_length=200)
    description : str = Field(min_length=6,max_length=500)
    role :str= Field(min_length=1,max_length=200)
    experience_in_years : int = Field(gt=-1)
    technology :str= Field(min_length=2,max_length=200)
    category:str= Field(min_length=2,max_length=200)
    title:str= Field(min_length=2,max_length=200)      
        
def create_profile(name: str, description : str, role:str,experience_in_years: int,
                technology: str, category:str, title:str,project_id:str,
                profile_repository: profile_repository.ProfileRepository)-> None:
    
    LOGGER.info("Creating profile with name [%s]", name)
    
    persisted_user = profile_repository.get_by_name(name = name)
    
    if persisted_user is not None:
        raise ProfileNameAlreadyExistError()
    
    
    profile_repository.save(
        profile = profile_model.Profile(
            name = name,
            technology = technology,
            role = role,
            experience_in_years = experience_in_years,
            category = category,
            title=title,
            description=description,
            project_id=project_id
            )
        )
    