import abc
from services.employee.model import employee_model
from typing import List, Optional

class EmployeeRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_person_id(self, person_id: str)-> Optional[employee_model.EmployeeReadModel]:
        ...
        
    @abc.abstractmethod
    def save(self, employee: employee_model.EmployeeCreateModel)-> None:
        ...
    
    #@abc.abstractmethod    
    #def delete_employee(self, person_id: int)-> Optional[int]:
        ...    
    #@abc.abstractmethod
    #def get_all_professionals(self):
    #    ...