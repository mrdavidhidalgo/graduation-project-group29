import abc
from typing import Optional,List
from services.interview.model import interview_model

class InterviewRepository(abc.ABC):
    

    def save(self, interview: interview_model.Interview)-> None:
        ...

    def get_by_project_and_candidate(self, project_name: str,candidate_document: str)-> Optional[interview_model.Interview]:
        ... 