from typing import Optional
from pydantic import BaseModel
import datetime

class User(BaseModel):
    username: str
    password: str
    is_active: str
    role: str
    person: int