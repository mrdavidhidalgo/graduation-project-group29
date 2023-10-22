from typing import Optional
from pydantic import BaseModel
import datetime

class EmployeeCreateModel(BaseModel):
    profile: str
    position: str
    person_id: int
    company_id: int 
    
class EmployeeReadModel(BaseModel):
    id: int
    profile: str
    position: str
    person_id: int
    company_id: int 
    