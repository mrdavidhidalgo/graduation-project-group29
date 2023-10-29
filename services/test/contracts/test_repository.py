import abc
from typing import Optional
from services.test.model import test_model

class TestRepository(abc.ABC):
    
    def get_by_name(self, name: str)-> Optional[test_model.Test]:
        ... 
        
    def save(self, test: test_model.Test)-> None:
        ...
