from services.technology.contracts import technology_repository
import pytest
from typing import Optional, List
from services.technology.model import technology_model
from services.technology import technology_service as subject
from datetime import datetime,timedelta,date
import os
import pytest

def test_create_technology_successfully():
    technology_request = subject.CreateTechnologyRequest(technology_name="JAVA", details="LENGUAJE DE PROGRAMACION JAVA", category="DEV")
    
    technology=subject.create_technology(request=technology_request, technology_repository=MockTechnology())
    assert technology is None

def test_create_technology_failed():
    with pytest.raises(subject.TechnologyAlreadyExistError):
        technology_request = subject.CreateTechnologyRequest(technology_name="PYTHON", details="LENGUAJE DE PROGRAMACION PYTHON", category="DEV")
        technology=subject.create_technology(request=technology_request, technology_repository=MockTechnology())
    #assert technology is None


def test_get_all_companies():
    technology=subject.get_all(technology_repository = MockTechnology(technology_with_params=technology_model.TechnologyRead(id="1"\
    ,technology_name="PYTHON",details ="LENGUAJE DE PROGRAMACION PYTHON",category="DEV")))
    assert technology is not None


def test_get_technology_by_name_with_value():
    technology=subject.get_by_name(technology_repository = MockTechnology(technology_with_params = technology_model.TechnologyRead(id="1"\
    ,technology_name="PYTHON",details ="LENGUAJE DE PROGRAMACION PYTHON",category="DEV")), technology_name="PYTHON" )
    assert technology.technology_name == "PYTHON"

def test_get_technology_by_name_not_exists():
    technology=subject.get_by_name(technology_repository = MockTechnology(technology_with_params = technology_model.TechnologyRead(id="1"\
    ,technology_name="PYTHON",details ="LENGUAJE DE PROGRAMACION PYTHON",category="DEV")), technology_name="JAVA" )
    assert technology is None

     
class MockTechnology(technology_repository.TechnologyRepository):
   
    def __init__(self,technology_by_id: technology_model.TechnologyCreate=None,technology_with_params:technology_model.TechnologyRead=None)->None:
       self.by_id=technology_by_id
       self.technology_with_params=technology_with_params
    
    def get_by_name(self, technology_name: str)->Optional[technology_model.TechnologyRead]:  
        return None if technology_name == "JAVA" else technology_model.TechnologyRead(id="1",
           technology_name="PYTHON",  details ="LENGUAJE DE PROGRAMACION PYTHON"
           ,category="DEV"
        )
    
    def get_all(self)-> Optional[List[technology_model.TechnologyRead]]:
        return self.technology_with_params
    
    def save(self, technology: technology_model.TechnologyCreate)-> None:
        return None
        
    def delete_technology(self, technology_id: int)-> Optional[int]:
        return 1
    

