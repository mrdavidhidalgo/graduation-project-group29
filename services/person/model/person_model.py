from typing import Optional
from pydantic import BaseModel
import datetime

class Person(BaseModel):
    document: int
    document_type: str
    first_name: str
    last_name: str
    phone_number: str