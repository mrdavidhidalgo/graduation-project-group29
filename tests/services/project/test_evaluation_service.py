from services.project.contracts import project_repository, member_repository, performance_evaluation_repository
from services.person.contracts import person_repository
from services.employee.contracts import employee_repository
import pytest
from typing import Optional, List
from services.project.model import project_model, member_model, performance_evaluation_model
from services.person.model import person_model
from services.employee.model import employee_model
from datetime import datetime,timedelta,date
import os
from services import logs

data_test=datetime.now().replace(microsecond=0)
data_test2=datetime.now().date()

 
LOGGER = logs.get_logger()


def test_create_member_successfully():
    from services.project import performance_evaluation_service as subject
    
    evaluation_request = subject.CreateEvaluationRequest(score="8", details="Buen desempeño",project_id="3", person_document="12345",
    member_id="5")
    
    evaluation=subject.create_evaluation(request= evaluation_request, person_id = "98765", performance_evaluation_repository=MockPerformanceEvaluation(), 
    employee_repository=MockEmployee(employee_with_params = \
    employee_model.EmployeeReadModel(id = 2, profile = "OPERATIVO" , position= "JEFE SOPORTE",\
    person_id = "98765", company_id = "4388827")), person_repository = MockPerson(person_with_params = \
    person_model.Person(document="12345", document_type="CC",first_name="PEDRO MARTIN", last_name="GOMEZ", phone_number="24234234"
    )) , member_repository=MockMember(member_with_params = \
    member_model.MemberRead(id=1, active=1, description="Nuevo miembro", person_id="12345",
    profile_id="Arquitecto Web 2", project_id="3"))
    )
    assert evaluation is None

def test_get_evaluations_by_project_id():
    from services.project import performance_evaluation_service as subject
    
    evaluations=subject.get_evaluations_by_project_id("1","98765",  performance_evaluation_repository=
    MockPerformanceEvaluation(evaluation_with_params=performance_evaluation_model.PerformanceEvaluationRead(id="1", score="8", 
    details="Buen desempeño",creation_date="2023-11-01", project_id="3", person_id="12345",
    member_id="5")),employee_repository=MockEmployee(employee_with_params = \
    employee_model.EmployeeReadModel(id = 2, profile = "OPERATIVO" , position= "JEFE SOPORTE",\
    person_id = "98765", company_id = "4388827")), person_repository = MockPerson(person_with_params = \
    person_model.Person(document="12345", document_type="CC",first_name="PEDRO MARTIN", last_name="GOMEZ", phone_number="24234234"
    )))
    assert evaluations[0].id == 1


"""
def test_get_evaluations_by_member_id():
    from services.project import performance_evaluation_service as subject
    
    evaluations=subject.get_evaluations_by_member_id("1","98765", "12345",  performance_evaluation_repository=
    MockPerformanceEvaluation(evaluation_with_params=performance_evaluation_model.PerformanceEvaluationRead(id="1", score="8", 
    details="Buen desempeño",creation_date="2023-11-01", project_id="3", person_id="12345",
    member_id="5")),employee_repository=MockEmployee(employee_with_params = \
    employee_model.EmployeeReadModel(id = 2, profile = "OPERATIVO" , position= "JEFE SOPORTE",\
    person_id = "98765", company_id = "4388827")), person_repository = MockPerson(person_with_params = \
    person_model.Person(document="12345", document_type="CC",first_name="PEDRO MARTIN", last_name="GOMEZ", phone_number="24234234"
    )))
    assert evaluations[0].id == 1

"""

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
    def get_all(self)->List[member_model.MemberRead]:
        return []
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

class MockPerformanceEvaluation(performance_evaluation_repository.PerformanceEvaluationRepository):
    def __init__(self, person_id: Optional[str]=None, evaluation_by_id:performance_evaluation_model.PerformanceEvaluationRead=None,
    evaluation_with_params:performance_evaluation_model.PerformanceEvaluationRead=None)->None:
       self.by_id=evaluation_by_id
       self.evaluation_with_params=evaluation_with_params
       self.person_id = person_id
   
    def create_evaluation(self, evaluation: performance_evaluation_model.PerformanceEvaluationCreate)-> str:
        return "1"
    
    def get_by_person_id(self, person_id: str, project_id: str)-> Optional[performance_evaluation_model.PerformanceEvaluationRead]:
        return None if person_id is None else self.evaluation_with_params
    
    def get_by_project_id(self, project_id: str)->Optional[List[performance_evaluation_model.PerformanceEvaluationRead]]:
        return None if project_id is None else [self.evaluation_with_params]
        
    def save(self, evaluation: performance_evaluation_model.PerformanceEvaluationCreate)-> None:
        return None
        