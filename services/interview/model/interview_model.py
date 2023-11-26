from typing import Optional
from pydantic import BaseModel
import  datetime
import enum


from typing import Optional,List
from pydantic import BaseModel
 


class Interview(BaseModel):
    candidate_document : str 
    project_id : str
    profile_id: str
    status : str
    meet_url : str
    start_timestamp : datetime.datetime
    duration_minutes: int



class AbilityInterviewInfo(BaseModel):
    ability_id: int
    qualification: int

class LoadInterviewInfo(BaseModel):
    candidate_document : str 
    project_id : str
    profile_id: str
    date: datetime.date
    recording_file: Optional[str]
    test_file : Optional[str]
    observation: str
    abilities: List[AbilityInterviewInfo]
    