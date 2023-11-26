from cgitb import reset
from services import logs
from services.interview.contracts import interview_repository
from services.interview.model import interview_model
from datetime import date
from typing import List, Tuple
from pydantic import BaseModel
from datetime import datetime
LOGGER = logs.get_logger()

class InterviewAlreadyExistError(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__("Error trying to create interview")
        
        
        
def create_interview(candidate_document: str, project_id: str,meet_url:int, status : str, 
                start_timestamp : date ,duration_minutes: int,profile_id : str,
                interview_repository: interview_repository.InterviewRepository)-> None:
    
    LOGGER.info("Creating interview for project id [%s]", project_id)
    
    persisted_interview = interview_repository.get_by_project_and_candidate(project_id=project_id,
                                                                            profile_id=profile_id,
                                                                            candidate_document=candidate_document)
    
    if persisted_interview is not None:
        raise InterviewAlreadyExistError()
    

    interview_repository.save(
        interview = interview_model.Interview(
            candidate_document = candidate_document,
            profile_id=profile_id,
            project_id = project_id,
            status = status,
            meet_url = meet_url,
            start_timestamp = start_timestamp,
            duration_minutes=duration_minutes,
            )
        )

class Interview(BaseModel):
    candidate_document : str 
    project_id : str
    profile_id: str 
    status : str
    meet_url : str 
    start_timestamp : datetime 
    duration_minutes: int

def get_interviews(candidate_document: str|None, 
                    interview_repository: interview_repository.InterviewRepository)-> List[Interview]:
    
    result = interview_repository.get_interviews(candidate_document)
    
    return result if result is None else [Interview(**i.dict()) for i in result ]


def load_interview(interview_info: interview_model.LoadInterviewInfo, interview_repository: interview_repository.InterviewRepository)->None:
    
    return interview_repository.load_interview(interview_info=interview_info)



class AbilityInterviewInfo(BaseModel):
    ability_id: int
    qualification: int

class LoadInterviewInfo(BaseModel):
    id:int|None=None 
    candidate_document : str 
    project_id : str
    profile_id: str
    date: date
    recording_file: str | None
    test_file : str | None
    observation: str
    abilities: List[AbilityInterviewInfo]
    

def find_interview_results(interview_repository: interview_repository.InterviewRepository)->List[interview_model.LoadInterviewInfo]:
    return interview_repository.find_interview_results()


def find_interview_result(id:int,interview_repository: interview_repository.InterviewRepository)-> interview_model.LoadInterviewInfo | None:
    return interview_repository.find_interview_result(id)