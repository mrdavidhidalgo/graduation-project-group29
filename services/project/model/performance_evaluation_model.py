from typing import Optional
from pydantic import BaseModel
import datetime
from services.commons import base

class PerformanceEvaluationCreate(BaseModel):
    score : str
    details : str
    project_id : str
    person_id : str
    member_id : str

class PerformanceEvaluationRead(BaseModel):
    id : int
    score : str
    details : str
    creation_date : str
    project_id : str
    person_id : str
    member_id : str