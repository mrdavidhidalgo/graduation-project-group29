from typing import Optional
from pydantic import BaseModel
import datetime
import enum

class UserRole(enum.Enum):
    CANDIDATE = enum.auto()
    RECRUITER = enum.auto()
    CLIENT = enum.auto()
    ADMINISTRATOR = enum.auto()

class User(BaseModel):
    username: str
    password: str
    is_active: bool
    role: UserRole
    person_id: str