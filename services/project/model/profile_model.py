
from pydantic import BaseModel
 


class Profile(BaseModel):
    name : str
    description : str 
    role :str
    experience_in_years : int
    technology :str
    category:str
    title:str   
    project_id:str