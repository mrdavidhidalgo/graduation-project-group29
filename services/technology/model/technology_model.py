from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class TechnologyCreate(BaseModel):
    technology_name : str
    details : str
    category : base.TechnologyCategory
   
    
class TechnologyRead(BaseModel):    
    id : int
    technology_name : str
    details : str
    category : base.TechnologyCategory
