import abc
from services.project.model import performance_evaluation_model
from typing import List, Optional

class PerformanceEvaluationRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_person_id(self, person_id: str)-> performance_evaluation_model.PerformanceEvaluationRead:
        ...
    
    @abc.abstractmethod
    def get_by_project_id(self, project_id: str)-> Optional[List[performance_evaluation_model.PerformanceEvaluationRead]]:
        ...
        
    @abc.abstractmethod
    def save(self, evaluation: performance_evaluation_model.PerformanceEvaluationCreate)-> None:
        ...
        
    #@abc.abstractmethod
    #def get_all(self)->List[member_model.MemberRead]:
    #    ...
