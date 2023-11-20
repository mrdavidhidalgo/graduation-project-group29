from typing import List, Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class ProfessionalCreateModel(BaseModel):
    birth_date: str
    age: int
    origin_country: base.Country
    residence_country: base.Country
    residence_city: str
    address: str
    person_id: str
    
class ProfessionalReadModel(BaseModel):
    id: int
    birth_date: str
    age: int
    origin_country: base.Country
    residence_country: base.Country
    residence_city: str
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
    

class AbilityInterviewInfo(BaseModel):
    ability_id: int
    qualification: int

class LoadInterviewInfo(BaseModel):
    professional_id : int
    date: datetime.datetime
    recording_file: Optional[str]
    test_file : Optional[str]
    observation: str
    abilities: List[AbilityInterviewInfo]
    

    

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
    
class ProfessionalTechnologyInfo(BaseModel):
    person_id : str
    name: str
    experience_years: int
    level: int
    description : str
    
class ProfessionalFullInfo(BaseModel):
    basic_info: ProfessionalReadModel
    academic_info: List[ProfessionalAcademicInfo]
    laboral_info: List[ProfessionalLaboralInfo]
    technology_info: List[ProfessionalTechnologyInfo]
    
class ProfessionalTechnicalRole(BaseModel):
    person_id : str
    role: str
    experience_years: int
    description : str

class ProfessionalSearchResult(BaseModel):
    person_id: str
    first_name: str
    last_name: str
    age: int
    roles: str
    titles: str
    technologies: str
    abilities: str
    score: str

class ProfessionalSearchRequest(BaseModel):
    role_filter: str
    role: str
    role_experience: str
    technologies: list = []
    abilities: list = []
    titles: list = []
    title_filter: str
    title: str
    title_experience: str