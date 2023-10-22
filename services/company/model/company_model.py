from typing import Optional
from pydantic import BaseModel
import datetime

class Company(BaseModel):
    taxpayerId: str
    name: str
    country: str
    city: str
    years: str
    address: str
    phoneNumber: str