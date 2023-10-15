from typing import Optional
from pydantic import BaseModel
import datetime

class ProfessionalCreateModel(BaseModel):
    birthDate: str
    age: int
    originCountry: str
    residenceCountry: str
    residenceCity: str
    address: str
    person_id: str
    
class ProfessionalReadModel(BaseModel):
    id: int
    birthDate: str
    age: int
    originCountry: str
    residenceCountry: str
    residenceCity: str
    address: str
    person_id: str
    
class ProfessionalAcademicInfo(BaseModel):
    person_id : str
    title : str
    institution : str
    country : str
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str