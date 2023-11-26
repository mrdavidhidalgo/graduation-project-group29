import abc
from services.project.model import member_model
from typing import List, Optional

class MemberRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_member_id(self, person_id: str)-> member_model.MemberRead:
        ...
    
    @abc.abstractmethod
    def get_by_project_id(self, project_id: str)-> member_model.MemberRead:
        ...
        
    @abc.abstractmethod
    def save(self, member: member_model.MemberCreate)-> None:
        ...
        
    @abc.abstractmethod
    def get_all(self)->List[member_model.MemberRead]:
        ...