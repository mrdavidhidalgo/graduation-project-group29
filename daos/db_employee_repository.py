from typing import Optional
from .db_model import db_model as models

from services.employee.contracts import employee_repository

from sqlalchemy.orm import Session

from services.employee.model import employee_model

class DBEmployeeRepository(employee_repository.EmployeeRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_person_id(self, person_id: str)-> Optional[employee_model.EmployeeReadModel]:
        employee = self.db.query(models.Employee).filter(models.Employee.person_id == person_id).first()
       
        return None if employee is None else employee_model.EmployeeReadModel(id = employee.id, profile = employee.profile , position=employee.position,\
        person_id = person_id, company_id = employee.company_id )
        
    def save(self, employee: employee_model.EmployeeCreateModel)-> None:
        new_employee = models.Employee(
            profile = employee.profile,
            position = employee.position,
            person_id = employee.person_id,
            company_id =  employee.company_id
        )
        
        self.db.add(new_employee)
        self.db.commit()