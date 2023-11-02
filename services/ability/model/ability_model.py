from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class AbilityCreate(BaseModel):
    ability_name : str
    details : str
    category : base.AbilityCategory
   
    
class AbilityRead(BaseModel):
    id : int
    ability_name : str
    details : str
    category : base.AbilityCategory
