import abc
from services.project.model import project_model
from typing import List, Optional

class ProjectRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_project_id(self, project_id: str)-> project_model.ProjectRead:
        ...
    
    @abc.abstractmethod
    def get_by_project_name(self, project_name: str, company_id: int)-> project_model.ProjectRead:
        ...
        
    @abc.abstractmethod
    def save(self, project: project_model.ProjectCreate)-> None:
        ...
        
    @abc.abstractmethod
    def get_all(self)->List[project_model.ProjectRead]:
        ...
    
    @abc.abstractmethod
    def get_projects_by_company_id(self,company_id: str)->Optional[List[project_model.ProjectRead]]:
        ...
        
    #@abc.abstractmethod    
    #def delete_project(self, project_id: int)-> Optional[int]:
    #    ...