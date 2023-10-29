from typing import Optional
from pydantic import BaseModel
from  datetime import date
import enum


class Test(BaseModel):
    name : str
    technology : str
    duration_minutes : int
    status : str
    start_date : date 
    end_date: date
    description : str