from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class ProfessionalCreateModel(BaseModel):
    birthDate: str
    age: int
    originCountry: base.Country
    residenceCountry: base.Country
    residenceCity: str
    address: str
    person_id: str
    
class ProfessionalReadModel(BaseModel):
    id: int
    birthDate: str
    age: int
    originCountry: base.Country
    residenceCountry: base.Country
    residenceCity: str
    address: str
    person_id: str
    
class ProfessionalAcademicInfo(BaseModel):
    person_id : str
    title : str
    institution : str
    country : base.Country
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str
    

class ProfessionalLaboralInfo(BaseModel):
    person_id : str
    position: str
    company_name: str
    company_country: base.Country
    company_address: str
    company_phone: str
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str