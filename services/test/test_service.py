from services import logs
from services.test.contracts import test_repository
from services.test.model import test_model
from datetime import date

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