from services import logs
from services.test.contracts import test_repository
from services.test.model import test_model
from datetime import date
from typing import List, Tuple
LOGGER = logs.get_logger()

class TestNameAlreadyExistError(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__("Error trying to create test")
        
        
        
def create_test(name: str, technology: str,duration_minutes:int, status : str, 
                start_date : date ,end_date: date,description : str, 
                test_repository: test_repository.TestRepository)-> None:
    
    LOGGER.info("Creating test with name [%s]", name)
    
    persisted_user = test_repository.get_by_name(name = name)
    
    if persisted_user is not None:
        raise TestNameAlreadyExistError()
    
    
    test_repository.save(
        test = test_model.Test(
            name = name,
            technology = technology,
            duration_minutes = duration_minutes,
            status = status,
            start_date = start_date,
            end_date=end_date,
            description=description
            )
        )

def get_tests(test_repository: test_repository.TestRepository)-> None:
    
    LOGGER.info("Getting tests")
    
    return test_repository.get_tests()


     
def register_result_tests(results: List[Tuple[str,str,str|None,int]],test_repository: test_repository.TestRepository)-> None:
    
    LOGGER.info("Registering test results for [%s]", len(results))
    
    result = [test_model.TestResult(test_name=r[0],candidate_document=r[1],observation=r[2],points=r[3]) for r in results]

    test_repository.save_results(result)