from services.ability.contracts import ability_repository
import pytest
from typing import Optional, List
from services.ability.model import ability_model
from services.ability import ability_service as subject
from datetime import datetime,timedelta,date
import os
import pytest

def test_create_ability_successfully():
    ability_request = subject.CreateAbilityRequest(ability_name="LIDERAZGO", details="CAPCIDAD PARA LIDERAR EQUIPOS", category="SOFT")
    
    ability=subject.create_ability(request=ability_request, ability_repository=MockAbility())
    assert ability is None

def test_create_ability_failed():
    with pytest.raises(subject.AbilityAlreadyExistError):
        ability_request = subject.CreateAbilityRequest(ability_name="COLABORACION", details="CAPCIDAD PARA AYUDAR A EQUIPOS", category="SOFT")
        ability=subject.create_ability(request=ability_request, ability_repository=MockAbility())
    #ability2=subject.create_ability(request=ability_request, ability_repository=MockAbility())
    #assert ability is not None

def test_get_all_abilities():
    ability=subject.get_all(ability_repository = MockAbility(ability_with_params=ability_model.AbilityRead(id="1"\
    ,ability_name="LIDERAZGO",details ="CAPCIDAD PARA LIDERAR EQUIPOS",category="SOFT")))
    assert ability is not None


def test_get_ability_by_name_with_value():
    ability=subject.get_by_name(ability_repository = MockAbility(ability_with_params = ability_model.AbilityRead(id="1"\
    ,ability_name="COLABORACION", details="CAPCIDAD PARA AYUDAR A EQUIPOS", category="SOFT")), ability_name="COLABORACION")
    assert ability.ability_name == "COLABORACION"

"""def test_get_technology_by_name_not_exists():
    ability=subject.get_by_name(technology_repository = MockTechnology(technology_with_params = technology_model.TechnologyRead(id="1"\
    ,technology_name="PYTHON",details ="LENGUAJE DE PROGRAMACION PYTHON",category="DEV")), technology_name="JAVA" )
    assert technology.technology_name != "JAVA"
"""

     
class MockAbility(ability_repository.AbilityRepository):
   
    def __init__(self,ability_by_id: ability_model.AbilityCreate=None,ability_with_params:ability_model.AbilityRead=None)->None:
       self.by_id=ability_by_id
       self.ability_with_params=ability_with_params
    
    def get_by_name(self, ability_name: str)->Optional[ability_model.AbilityRead]:  
        return None if ability_name == "LIDERAZGO" else ability_model.AbilityRead(id="1",
           ability_name="COLABORACION",  details ="CAPCIDAD PARA LIDERAR EQUIPOS"
           ,category="SOFT"
        )
    
    def get_all(self)-> Optional[List[ability_model.AbilityRead]]:
        return self.ability_with_params
    
    def save(self, technology: ability_model.AbilityCreate)-> None:
        return None
        
    def delete_ability(self, ability_id: int)-> Optional[int]:
        return 1
    


