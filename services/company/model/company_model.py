from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class Company(BaseModel):
    taxpayer_id: str
    name: str
    country: base.Country
    city: str
    years: str
    address: str
    phone_number: str