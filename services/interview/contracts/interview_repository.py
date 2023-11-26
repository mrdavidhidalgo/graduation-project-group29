import abc
from typing import Optional,List
from services.interview.model import interview_model

class InterviewRepository(abc.ABC):
    

    def save(self, interview: interview_model.Interview)-> None:
        ...

    def get_by_project_and_candidate(self, project_id: str,candidate_document: str,profile_id:str)-> Optional[interview_model.Interview]:
        ... 


    def get_interviews(candidate_document: str|None)-> List[interview_model.Interview]:
        ...

    @abc.abstractmethod
    def load_interview(self, interview_info: interview_model.LoadInterviewInfo)->None:
        ...