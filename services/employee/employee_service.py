

from datetime import timedelta
import datetime
from typing import List, Optional

#from .contracts import user_repository
from services.employee.contracts import employee_repository
from services.user.contracts import user_repository
from services.employee.model import employee_model



from services import logs


LOGGER = logs.get_logger()

                
class EmployeeAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "The person already exists as a employee"
        super().__init__(self.message)
        
class EmployeeDoesNotExistError(Exception):
     def __init__(self, person_id: str, *args: object) -> None:
        self.message = f"The Employee with personID {person_id} does not exist"
        super().__init__(self.message)
    

def create_employee(profile: str, position: str, company_id: str, person_id: str,  
                        employee_repository: employee_repository.EmployeeRepository)-> None:
    
    LOGGER.info("Creating employee for person_id [%s]", person_id)
    
    persisted_employee = employee_repository.get_by_person_id(person_id = person_id)
    
    if persisted_employee is not None:
        raise EmployeeAlreadyExistError()
    
    employee_repository.save(
        employee = employee_model.EmployeeCreateModel(
            profile = profile,
            position = position,
            company_id = company_id,
            person_id = person_id )
        )
        
def get_by_person_id(employee_repository: employee_repository.EmployeeRepository, person_id: str)-> Optional[employee_model.EmployeeReadModel]:
    LOGGER.info("Search employees in service wirh person_id= [%s]", person_id)
    list =  employee_repository.get_by_person_id(person_id = person_id)
    if list is None:
        LOGGER.info("Empty List in employee service")
        raise EmployeeDoesNotExistError(person_id = person_id)
    else:
        LOGGER.info("Employee exists in service")
        return list