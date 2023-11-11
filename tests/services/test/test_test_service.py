
from services.test.contracts import test_repository
from typing import Optional, List
from services.test.model import test_model
from datetime import datetime,timedelta,date
import os
import pytest


class MockTest(test_repository.TestRepository):
    
    def __init__(self):
        super().__init__()
    
    def get_by_name(self, name: str)-> Optional[test_model.Test]:
        if name == "error":
            return test_model.Test(name= "", technology="JAVA",duration_minutes=5, status="ENABLED", 
                start_date = date.fromisoformat('2019-12-04') ,end_date= date.fromisoformat('2019-12-04'),description ="description")
        return None
    
    def save(self, test: test_model.Test)-> None:
        return None

    def get_tests(self)-> List[test_model.Test]:
        return []

    def save_results(self,results:List[test_model.TestResult])->None:
        return None   

def test_create_test_successfully():
    from services.test import test_service as subject
    
    test = subject.create_test(name= "Test1 ", technology="JAVA",duration_minutes=5, status="ENABLED", 
                start_date = date.fromisoformat('2019-12-04'),end_date= date.fromisoformat('2019-12-04'),description ="description", 
                test_repository= MockTest())
    
    assert test is None
    
def test_create_test_already_exist(): 
    from services.test import test_service as subject
    
    with pytest.raises(subject.TestNameAlreadyExistError):
        subject.create_test(name= "error", technology="JAVA",duration_minutes=5, status="ENABLED", 
                    start_date = date.fromisoformat('2019-12-04') ,end_date= date.fromisoformat('2019-12-04'),description ="description", 
                    test_repository= MockTest())

def test_register_test_successfully():
    from services.test import test_service as subject
    
    result = [("Test 1","1234","observation",80)]

    test = subject.register_result_tests(result,test_repository= MockTest())
    
    assert test is None
        
