from typing import Optional
from pydantic import BaseModel
from  datetime import date
import enum


from typing import Optional
from pydantic import BaseModel
from  datetime import datetime


class Interview(BaseModel):
    candidate_document : str 
    project_name : str
    status : str
    meet_url : str
    start_timestamp : datetime 
    duration_minutes: int