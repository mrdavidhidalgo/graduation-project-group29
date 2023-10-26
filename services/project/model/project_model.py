from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class ProjectCreate(BaseModel):
    project_name : str
    start_date : datetime.date
    active : bool
    details : str
    company_id : str
    
class ProjectRead(BaseModel):    
    id : int
    project_name : str
    start_date : datetime.date
    active : bool
    creation_time : datetime.datetime
    details : str
    company_id : str