from services.project.contracts import project_repository
from services.user.contracts import user_repository
from services.employee.contracts import employee_repository
import pytest
from typing import Optional, List
from services.project.model import project_model
from services.user.model import user_model
from services.employee.model import employee_model
from datetime import datetime,timedelta,date
import os
from services import logs

data_test=datetime.now().replace(microsecond=0)
data_test2=datetime.now().date()

 
LOGGER = logs.get_logger()


def test_create_project_successfully():
    from services.project import project_service as subject
    
    project_request = subject.CreateProjectRequest(project_name="BAC Jobs", start_date=data_test2,active=1,
    details="Proyecto desarrollo web y python")
    
    project=subject.create_project(request=project_request, person_id = "1234567", project_repository=MockProject(), employee_repository=MockEmployee())
    assert project is None

def test_get_all_projects():
    from services.project import project_service as subject

    project=subject.get_all(project_repository=MockProject(project_with_params = \
    project_model.ProjectRead(id=1, project_name="BAC Jobs", start_date=data_test2, active=1, creation_time=data_test,\
    details="Proyecto desarrollo web y python",company_id="323477234")))
    assert project is not None


def test_get_project_by_id_with_value():
    from services.project import project_service as subject
    project=subject.get_by_project_name(project_repository=MockProject(project_with_params = \
    project_model.ProjectRead(id=1, project_name="BAC Jobs", start_date=data_test2 ,active=1, creation_time=data_test,\
    details="Proyecto desarrollo web y python",company_id="323477234")), project_name="BAC Jobs", company_id= 323477234)
    assert project.id == 1

def test_get_projects_by_company():
    from services.project import project_service as subject
    project=subject.get_projects_by_company_id("1", project_repository=MockProject(project_with_params = \
    project_model.ProjectRead(id=1, project_name="BAC Jobs", start_date=data_test2 ,active=1, creation_time=data_test,\
    details="Proyecto desarrollo web y python",company_id="323477234")), employee_repository=MockEmployee(employee_with_params = \
    employee_model.EmployeeReadModel(id = 2, profile = "OPERATIVO" , position= "JEFE SOPORTE",\
        person_id = "1", company_id = "4388827")))
    assert project.id == 1

class MockProject(project_repository.ProjectRepository):
   
    def __init__(self,project_by_id: project_model.ProjectRead=None,project_with_params:project_model.ProjectRead=None)->None:
       self.by_id=project_by_id
       self.project_with_params=project_with_params
   
    def create_project(self, project: project_model.ProjectCreate)-> str:
        return "1"
    
    def get_by_project_id(self, project_id: str)-> str:
        return self.by_id
        
    def get_by_project_name(self, project_name: str, company_id: int)-> project_model.ProjectRead:
        return self.project_with_params
    
    def get_all(self)->List[project_model.ProjectRead]:
        return self.project_with_params
    
    def save(self, project: project_model.ProjectCreate)-> None:
        return None
        
    def delete_project(self, project_id: int)-> Optional[int]:
        return 1
    
    def get_projects_by_company_id(self,company_id: str)->Optional[List[project_model.ProjectRead]]:
        return self.project_with_params
        
class MockEmployee(employee_repository.EmployeeRepository):
   
    def __init__(self, person_id: Optional[str]=None, employee_by_id: employee_model.EmployeeCreateModel=None,employee_with_params:employee_model.EmployeeCreateModel=None)->None:
       self.by_id=employee_by_id
       self.employee_with_params=employee_with_params
       self.person_id = person_id
   
    def create_employee(self, employee: employee_model.EmployeeCreateModel)-> str:
        return "1"
    
    def get_by_person_id(self, person_id: str)-> Optional[employee_model.EmployeeReadModel]:
        print("Buscando %s - %s", person_id, self.person_id)
        return None if person_id is None else employee_model.EmployeeReadModel(id = 2, profile = "OPERATIVO" , position= "JEFE SOPORTE",\
        person_id = person_id, company_id = "4388827")
    
    def save(self, employee: employee_model.EmployeeCreateModel)-> None:
        return None
        
    def delete_employee(self, person_id: int)-> Optional[int]:
        return 1