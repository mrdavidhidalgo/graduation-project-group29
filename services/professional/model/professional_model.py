from typing import Optional
from pydantic import BaseModel
import datetime

class Professional(BaseModel):
    birthDate: str
    age: int
    originCountry: str
    residenceCountry: str
    residenceCity: str
    address: str
    person_id: int