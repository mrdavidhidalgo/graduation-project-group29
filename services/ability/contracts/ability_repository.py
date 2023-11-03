import abc
from services.ability.model import ability_model
from typing import List, Optional

class AbilityRepository(abc.ABC):
    
    @abc.abstractmethod
    def save(self, ability: ability_model.AbilityCreate)-> None:
        ...
        
    @abc.abstractmethod
    def get_all(self)->List[ability_model.AbilityRead]:
        ...
    
    @abc.abstractmethod
    def get_by_name(self, ability_name: str)-> ability_model.AbilityRead:
        ...
