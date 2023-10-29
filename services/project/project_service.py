

from datetime import timedelta
import datetime
from typing import List, Optional

from services.project.contracts import project_repository
from services.user.contracts import user_repository
from services.company.contracts import company_repository
from services.employee.contracts import employee_repository
from services.employee import employee_service
from services.user.model import user_model
from services.project.model import project_model
from services.user import user_service
from services.project import project_service
from services.company import company_service
from pydantic import BaseModel


import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class ProjectNameAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Project Name  is already used"
        super().__init__(self.message)
        
class CreateProjectRequest(BaseModel):
    project_name : str
    start_date : datetime.date
    active : bool
    details : str

def create_project(request : CreateProjectRequest, person_id: str, project_repository: project_repository.ProjectRepository,\
employee_repository: employee_repository.EmployeeRepository)-> None:
    
    LOGGER.info("Creating Project with Name [%s]", request.project_name)
    
    employee_project = employee_service.get_by_person_id(employee_repository, person_id = person_id)
    if employee_project is None:
        raise employee_service.EmployeeDoesNotExistError()
    
    persisted_project = project_repository.get_by_project_name(project_name = request.project_name, company_id = employee_project.company_id)
    
    if persisted_project is not None:
        raise ProjectNameAlreadyExistError()
    
    
    project_repository.save(
        project=project_model.ProjectCreate(
            project_name=request.project_name,
            start_date=request.start_date,
            active=request.active,
            details=request.details,
            company_id=str(employee_project.company_id)
            )
        )
    
    
    
def get_by_project_name(project_repository: project_repository.ProjectRepository, project_name: str, company_id: str)-> Optional[project_model.ProjectRead]:
    LOGGER.info("Search for project by id")
    project = project_repository.get_by_project_name(project_name = project_name, company_id = company_id)
    if project is None:
        LOGGER.info("Project not exists")
        return None
    else:
        LOGGER.info("Project exists in service")
        return project
        
def get_all(project_repository: project_repository.ProjectRepository)->List[project_model.ProjectRead]:
    LOGGER.info("Search for projects in service")
    list = project_repository.get_all()
    if list is None:
        LOGGER.info("Empty List project in service")
        return None
    else:
        LOGGER.info("Project List with data in service")
        return list
