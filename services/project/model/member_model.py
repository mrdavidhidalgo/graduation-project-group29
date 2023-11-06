from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class MemberCreate(BaseModel):
    active : bool
    description : str
    person_id : str
    profile_id : str
    project_id : str
    
class MemberRead(BaseModel):    
    id :int
    active : bool
    description : str
    person_id : str
    profile_id : str
    project_id : str
