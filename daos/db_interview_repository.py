from typing import Optional
from .db_model import db_model as models

from services.interview.contracts import interview_model
from typing import List
from sqlalchemy.orm import Session

from services.interview.contracts import interview_repository

class DBInterviewRepository(interview_repository.InterviewRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
    def get_by_project_and_candidate(self, project_name: str,candidate_document: str)-> Optional[interview_model.Interview]:
        ... 
        interv = self.db.query(models.Interview).filter(models.Interview.candidate_document == candidate_document and models.Interview.project_name == project_name ).first() 
        
        return None if interv is None else interview_model.Interview(    
                                                         candidate_document = interv.candidate_document,
                                                         project_name = interv.project_name,
                                                         status = interv.status,
                                                         meet_url = interv.meet_url,
                                                         start_timestamp = interv.start_timestamp,
                                                         duration_minutes = interv.duration_minutes)
        
    def save(self, interview: interview_model.Interview)-> None:
        new_interview = models.Interview(**interview.dict())
        
        self.db.add(new_interview)
        self.db.commit()
