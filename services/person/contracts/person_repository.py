import abc
from services.person.model import person_model
from typing import List

class PersonRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_document(self, document: str)-> person_model.Person:
        ...
        
    @abc.abstractmethod
    def save(self, person: person_model.Person)-> None:
        ...
        
    @abc.abstractmethod
    def get_all(self)->List[person_model.Person]:
        ...