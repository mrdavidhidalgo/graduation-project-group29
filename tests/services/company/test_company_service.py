from services.company.contracts import company_repository
from services.person.contracts import person_repository
from services.user.contracts import user_repository
from services.employee.contracts import employee_repository
import pytest
from typing import Optional, List
from services.company.model import company_model
from services.person.model import person_model
from services.user.model import user_model
from services.employee.model import employee_model
from datetime import datetime,timedelta,date
import os


def test_create_company_successfully():
    from services.company import company_service as subject
    
    company_request = subject.CreateCompanyRequest(document="32534634",document_type="CC", first_name="German",last_name="Martinez",
    username="cmra@aol.co",password="HRerv3498&.",taxpayer_id="3645645",name="TECNISOFT",country="CO",city="CALI",
    years="3",address="Calle 1 No 2-35", phone_number="32899837",profile="OPERATIVO",position="LIDER TECNICO")
    
    company=subject.create_company(request=company_request, person_repository=MockPerson(), user_repository=MockUser(),
    company_repository=MockCompany(), employee_repository=MockEmployee())
    assert company is None

def test_get_all_companies():
    from services.company import company_service as subject

    company=subject.get_all(company_repository = MockCompany(company_by_id = company_model.Company(taxpayer_id="1",name="TECNISOFT",country="CO",city="CALI",
    years="3",address="Calle 1 No 2-35",phone_number="32899837")))
    assert company is None


def test_get_company_by_id_with_value():
    from services.company import company_service as subject 
    company=subject.get_by_taxpayerId(company_repository = MockCompany(company_by_id = company_model.Company(taxpayer_id="111111",name="TECNISOFT",country="CO",city="CALI",
    years="3",address="Calle 1 No 2-35",phone_number="32899837")),taxpayer_id="111111")
    assert company.taxpayer_id == "111111"


def test_get_company_by_person_id_with_value():
    from services.company import company_service as subject 
    company=subject.get_by_person_Id(person_id="12345",company_repository = MockCompany(company_by_id = company_model.Company(taxpayer_id="111111",name="TECNISOFT",country="CO",city="CALI",
    years="3",address="Calle 1 No 2-35",phone_number="32899837")), employee_repository= MockEmployee(employee_with_params = 
    employee_model.EmployeeReadModel(id=1, profile="ADMINISTRATIVO", position="JEFE DE SOPORTE", person_id="12345", company_id="111111")), 
    person_repository=MockPerson(person_with_params = 
    person_model.Person(document="12345", document_type="CC",first_name="PEDRO MARTIN", last_name="GOMEZ", phone_number="24234234")),
    user_repository=MockUser(user_with_params = 
    user_model.User(username="pgomez@gmail.co", password="34235HGS", created_at='2001-02-01 00:00:01',is_active='Y', role=user_model.UserRole.CLIENT ,person_id ="12345")))
    assert company.taxpayer_id == "111111"

     
class MockCompany(company_repository.CompanyRepository):
   
    def __init__(self,company_by_id: company_model.Company=None,company_with_params:company_model.Company=None)->None:
       self.by_id=company_by_id
       self.company_with_params=company_with_params
   
    def create_company(self, company: company_model.Company)-> str:
        return "1"
    
    def get_by_taxpayerId(self, taxpayer_id: str)-> str:
        return self.by_id
    
    def get_all(self)-> Optional[List[company_model.Company]]:
        return self.company_with_params
    
    def save(self, company: company_model.Company)-> None:
        return None
        
    def delete_company(self, taxpayer_id: int)-> Optional[int]:
        return 1
    
class MockPerson(person_repository.PersonRepository):
   
    def __init__(self,person_by_id: person_model.Person=None,person_with_params:person_model.Person=None)->None:
       self.by_id=person_by_id
       self.person_with_params=person_with_params
   
    def get_by_document(self, document: int)->str:
        return self.person_with_params
    
    def save(self, person: person_model.Person)->str:
        return "1"
    
    def get_all(self)-> str:
        return "1"
        
    def create_person(self, company: company_model.Company)-> str:
        return "1"

    def delete_person(self, document: int)->int:
        return 1
        
class MockUser(user_repository.UserRepository):
   
    def __init__(self,user_by_id: user_model.User=None,user_with_params:user_model.User=None)->None:
       self.by_id=user_by_id
       self.user_with_params=user_with_params
   
    def create_user(self, user: user_model.User)-> str:
        return "1"
    
    def get_by_username(self, username: str)-> str:
        return None
    
    def save(self, user: user_model.User)-> None:
        return None
    
    def get_by_person_id(self, person_id: str)-> Optional[user_model.User]:
        return self.user_with_params
        
    def delete_user(self, username: str)-> Optional[int]:
        return 1
        
class MockEmployee(employee_repository.EmployeeRepository):
   
    def __init__(self,employee_by_id: employee_model.EmployeeCreateModel=None, employee_with_params:employee_model.EmployeeReadModel=None)->None:
       self.by_id=employee_by_id
       self.employee_with_params=employee_with_params
   
    def create_employee(self, employee: employee_model.EmployeeCreateModel)-> str:
        return "1"
    
    def get_by_person_id(self, person_id: str)-> Optional[employee_model.EmployeeReadModel]:
        return self.employee_with_params
    
    def save(self, employee: employee_model.EmployeeCreateModel)-> None:
        return None
        
    def delete_employee(self, person_id: int)-> Optional[int]:
        return 1