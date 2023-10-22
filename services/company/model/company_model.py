from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class Company(BaseModel):
    taxpayerId: str
    name: str
    country: base.Country
    city: str
    years: str
    address: str
    phoneNumber: str