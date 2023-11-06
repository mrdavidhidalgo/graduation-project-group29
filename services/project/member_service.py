

from datetime import timedelta
import datetime
from typing import List, Optional

from services.project.contracts import member_repository, project_repository, profile_repository
from services.employee.contracts import employee_repository
from services.project import project_service
from services.employee import employee_service
from services.project.model import member_model
from services.user import user_service
from pydantic import BaseModel


import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class ProjectMemberAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Project Member  exists in project"
        super().__init__(self.message)
        
class CreateMemberRequest(BaseModel):
    active : bool
    description : str
    person_id : str
    profile_id : str
    project_id : str

def create_member(request : CreateMemberRequest, person_id: str, member_repository: member_repository.MemberRepository,\
employee_repository: employee_repository.EmployeeRepository)-> None:
    
    #LOGGER.info("Creating Member with Person", str(request.person_id))
    
    employee_project = employee_service.get_by_person_id(employee_repository, person_id = person_id)
    if employee_project is None:
        raise employee_service.EmployeeDoesNotExistError()
    
    persisted_member = member_repository.get_by_member_id(person_id = person_id, project_id = request.project_id)
    
    if persisted_member is not None:
        raise ProjectMemberAlreadyExistError()
    
    
    member_repository.save(
        member=member_model.MemberCreate(
            active = request.active,
            description = request.description,
            person_id = request.person_id,
            profile_id = request.profile_id,
            project_id = request.project_id
            )
        )