from typing import Optional
from pydantic import BaseModel
import datetime

class Person(BaseModel):
    document: int
    documentType: str
    firstName: str
    lastName: str
    phoneNumber: str