from typing import Optional
from pydantic import BaseModel
import datetime

class User(BaseModel):
    username: str
    password: str
    name: str
    is_active : bool