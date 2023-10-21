from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class Person(BaseModel):
    document: int
    document_type: base.DocumentType
    first_name: str
    last_name: str
    phone_number: str