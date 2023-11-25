from services import logs
from services.interview.contracts import interview_repository
from services.interview.model import interview_model
from datetime import date
from typing import List, Tuple
LOGGER = logs.get_logger()

class InterviewAlreadyExistError(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__("Error trying to create interview")
        
        
        
def create_interview(candidate_document: str, project_name: str,meet_url:int, status : str, 
                start_timestamp : date ,duration_minutes: int,
                interview_repository: interview_repository.InterviewRepository)-> None:
    
    LOGGER.info("Creating interview for project name [%s]", project_name)
    
    persisted_interview = interview_repository.get_by_project_and_candidate(project_name=project_name,
                                                                            candidate_document=candidate_document)
    
    if persisted_interview is not None:
        raise InterviewAlreadyExistError()
    

    interview_repository.save(
        interview = interview_model.Interview(
            candidate_document = candidate_document,
            project_name = project_name,
            status = status,
            meet_url = meet_url,
            start_timestamp = start_timestamp,
            duration_minutes=duration_minutes,
            )
        )
