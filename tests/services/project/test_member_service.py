from services.project.contracts import project_repository, member_repository
from services.person.contracts import person_repository
from services.employee.contracts import employee_repository
import pytest
from typing import Optional, List
from services.project.model import project_model, member_model
from services.person.model import person_model
from services.employee.model import employee_model
from datetime import datetime,timedelta,date
import os
from services import logs

data_test=datetime.now().replace(microsecond=0)
data_test2=datetime.now().date()

 
LOGGER = logs.get_logger()


def test_create_member_successfully():
    from services.project import member_service as subject
    
    member_request = subject.CreateMemberRequest(active=1, description="Nuevo miembro", person_document="12345",
    profile_id="Arquitecto Web 2", project_id="3")
    
    member=subject.create_member(request=member_request, person_id = "12345", member_repository=MockMember(), employee_repository=MockEmployee())
    assert member is None
    
def test_get_members_by_project_id():
    from services.project import member_service as subject
    
    members=subject.get_members_by_project_id("1","12345", member_repository=MockMember(member_with_params = \
    member_model.MemberRead(id=1, active=1, description="Nuevo miembro", person_id="12345",
    profile_id="Arquitecto Web 2", project_id="3")), employee_repository=MockEmployee(employee_with_params = \
    employee_model.EmployeeReadModel(id = 2, profile = "OPERATIVO" , position= "JEFE SOPORTE",\
    person_id = "12345", company_id = "4388827")), person_repository = MockPerson(person_with_params = \
    person_model.Person(document="12345", document_type="CC",first_name="PEDRO MARTIN", last_name="GOMEZ", phone_number="24234234"
    )))
    assert members[0].id == 1



class MockMember(member_repository.MemberRepository):
    def __init__(self, person_id: Optional[str]=None, member_by_id:member_model.MemberRead=None,member_with_params:member_model.MemberRead=None)->None:
       self.by_id=member_by_id
       self.member_with_params=member_with_params
       self.person_id = person_id
   
    def create_member(self, member: member_model.MemberCreate)-> str:
        return "1"
    
    def get_by_member_id(self, person_id: str, project_id: str)-> Optional[member_model.MemberRead]:
        return None if person_id is None else self.member_with_params
    
    def get_by_project_id(self, project_id: str)->Optional[List[member_model.MemberRead]]:
        return None if project_id is None else [self.member_with_params]
        
    def save(self, member: member_model.MemberCreate)-> None:
        return None
        
    def delete_employee(self, person_id: int)-> Optional[int]:
        return 1
        
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
        
class MockPerson(person_repository.PersonRepository):
   
    def __init__(self,person_by_id: person_model.Person=None,person_with_params:person_model.Person=None)->None:
       self.by_id=person_by_id
       self.person_with_params=person_with_params
   
    def get_by_document(self, document: int)->str:
        return None if document is None else self.person_with_params
    
    def save(self, person: person_model.Person)->str:
        return "1"
    
    def get_all(self)-> Optional[List[person_model.Person]]:
        return self.person_with_params

    def delete_person(self, document: int)->int:
        return 1  