import abc
from services.technology.model import technology_model
from typing import List, Optional

class TechnologyRepository(abc.ABC):
    
    @abc.abstractmethod
    def save(self, technology: technology_model.TechnologyCreate)-> None:
        ...
        
    @abc.abstractmethod
    def get_all(self)->List[technology_model.TechnologyRead]:
        ...
    
    @abc.abstractmethod
    def get_by_name(self, technology_name: str)-> technology_model.TechnologyRead:  
        ...