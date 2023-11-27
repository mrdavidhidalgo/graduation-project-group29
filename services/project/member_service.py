

from datetime import timedelta
import datetime
from typing import List, Optional,Set

from services.project.contracts import member_repository, project_repository
from services.person.contracts import person_repository
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

class ProjectMemberNotExistsError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Project Member does not exist in project"
        super().__init__(self.message)

   
class CreateMemberRequest(BaseModel):
    active : bool
    description : str
    person_document : str
    profile_id : str
    project_id : str


class ProjectMemberRequest(BaseModel):
    id : int
    active : str
    description : str
    person_id : str
    profile : str
    project_id : str
    member_name: str
    
def create_member(request : CreateMemberRequest, person_id: str, member_repository: member_repository.MemberRepository,\
employee_repository: employee_repository.EmployeeRepository)-> None:
    
    #LOGGER.info("Creating Member with Person", str(request.person_id))
    
    employee_project = employee_service.get_by_person_id(employee_repository, person_id = person_id)
    if employee_project is None:
        raise employee_service.EmployeeDoesNotExistError()
    
    persisted_member = member_repository.get_by_member_id(person_id = request.person_document, project_id = request.project_id)
    #LOGGER.info("Value of persisted_member [%s] in service", str(persisted_member))
    
    if persisted_member is not None:
        raise ProjectMemberAlreadyExistError()
    
    
    member_repository.save(
        member=member_model.MemberCreate(
            active = request.active,
            description = request.description,
            person_id = request.person_document,
            profile_id = request.profile_id,
            project_id = request.project_id
            )
        )

def get_members_by_project_id(project_id: str, person_id: str, member_repository: member_repository.MemberRepository,
    employee_repository: employee_repository.EmployeeRepository, person_repository: person_repository.PersonRepository
    )->Optional[List]:
    LOGGER.info("Search for members by project [%s] in service", str(project_id))
    
    employee_project = employee_service.get_by_person_id(employee_repository, person_id = person_id)
    if employee_project is None:
        raise employee_service.EmployeeDoesNotExistError()
    
    LOGGER.info("sending  to member repo [%s]", project_id)    
    
    members = member_repository.get_by_project_id(project_id=project_id)    
    
    if (members is None) or len(members) < 1:
        LOGGER.info("Empty List members in service")
        return None
    
    members_project_list = []
    member_create = ProjectMemberRequest
    for member in members:
        person = person_repository.get_by_document(member.person_id)
        member_create = ProjectMemberRequest(id  = member.id, active = str(member.active),
            description = member.description, person_id = member.person_id, 
            profile = member.profile_id, project_id = project_id,
            member_name = person.first_name + " " + person.last_name)
            
        members_project_list.append(member_create)
    
    LOGGER.info("Member List with data in service")
    return members_project_list


class ProfileAndProject(BaseModel):
    project_id : str
    project_name : str
    profile_names : List[str]

def get_profile_and_projects(member_repository: member_repository.MemberRepository,project_repository: project_repository.ProjectRepository) -> List[ProfileAndProject]:
    members=member_repository.get_all()
    projects=project_repository.get_all()
    result: Set[ProfileAndProject]= []
    projects_in_member = {p.id for p in projects}
    projects = [p for p in projects if p.id in projects_in_member]
    for project in projects:
        project_profiles = {m.profile_id for m in members if m.project_id == str(project.id)}
        if project_profiles:
            result.append(ProfileAndProject(project_id=str(project.id),project_name=project.project_name,profile_names=project_profiles))
    return result

