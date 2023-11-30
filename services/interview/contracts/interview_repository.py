import abc
from typing import Optional,List
from services.interview.model import interview_model

class InterviewRepository(abc.ABC):
    
    @abc.abstractmethod
    def save(self, interview: interview_model.Interview)-> None:
        ...
    @abc.abstractmethod
    def get_by_project_and_candidate(self, project_id: str,candidate_document: str,profile_id:str)-> Optional[interview_model.Interview]:
        ... 

    @abc.abstractmethod
    def get_interviews(candidate_document: str|None,status:str|None)-> List[interview_model.Interview]:
        ...

    @abc.abstractmethod
    def load_interview(interview_info: interview_model.LoadInterviewInfo)->None:
        ...

    @abc.abstractmethod
    def find_interview_results()->List[interview_model.LoadInterviewInfo]:
        ...

    @abc.abstractmethod
    def find_interview_result(id:int)-> interview_model.LoadInterviewInfo | None:
        ...

