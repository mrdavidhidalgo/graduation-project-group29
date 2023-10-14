import abc
from services.professional.model import professional_model
from typing import List

class ProfessionalRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_person_id(self, person_id: int)-> professional_model.Professional:
        ...
        
    @abc.abstractmethod
    def save(self, person: professional_model.Professional)-> None:
        ...
        
    #@abc.abstractmethod
    #def get_all_professionals(self):
    #    ...