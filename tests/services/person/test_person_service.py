
from services.person.contracts import person_repository
from services.user.contracts import user_repository
from services.professional.contracts import professional_repository
import pytest
from typing import Optional, List
from services.person.model import person_model
from services.user.model import user_model
from services.professional.model import professional_model
from datetime import datetime,timedelta,date
import os


def test_create_candidate_successfully():
    from services.person import person_service as subject
    
    candidate_request = subject.CreateCandidateRequest(document= "2343523",documentType= "CC",firstName= "Jorge",lastName= "Lopez",
	phoneNumber= "64345678",username= "jlopes453@gmail.com",password= "DHSc532XSC..",birthDate= "1989-12-11", age= "34",
        originCountry= "CO",residenceCountry= "AR", residenceCity= "Belgrano",address="Arroyito 14-11")
    
    candidate=subject.create_candidate(request=candidate_request, person_repository=MockPerson(), user_repository=MockUser(),
    professional_repository=MockProfessional())
    assert candidate is None

def test_get_all_persons():
    from services.person import person_service as subject

    person=subject.get_all(person_repository = MockPerson(person_by_id = person_model.Person(document= "2343523",document_type= "CC",first_name= "Jorge",last_name= "Lopez",
	phone_number= "64345678")))
    assert person is None

class MockPerson(person_repository.PersonRepository):
   
    def __init__(self,person_by_id: person_model.Person=None,person_with_params:person_model.Person=None)->None:
       self.by_id=person_by_id
       self.person_with_params=person_with_params
   
    def get_by_document(self, document: int)->str:
        return None
    
    def save(self, person: person_model.Person)->str:
        return "1"
    
    def get_all(self)-> Optional[List[person_model.Person]]:
        return self.person_with_params
        

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
        
class MockProfessional(professional_repository.ProfessionalRepository):
   
    def __init__(self,professional_by_id: professional_model.ProfessionalCreateModel=None,professional_with_params:professional_model.ProfessionalCreateModel=None)->None:
       self.by_id=professional_by_id
       self.professional_with_params=professional_with_params
    
    def get_by_person_id(self, person_id: str)-> Optional[professional_model.ProfessionalReadModel]:
        return None
    
    def save(self, professional: professional_model.ProfessionalCreateModel)-> None:
        return None
    
    def add_academic_info(self, professional_id: int, academic_info: professional_model.ProfessionalAcademicInfo)-> None:
        return None
        
    def add_laboral_info(self, professional_id: int, laboral_info: professional_model.ProfessionalLaboralInfo)-> None:
        return None
        
    def add_technical_role_info(self, professional_id: int, technical_role_info: professional_model.ProfessionalTechnicalRole)-> None:
        return None
        
    def add_technology_info(self, professional_id: int, technology_info: professional_model.ProfessionalTechnologyInfo)-> None:
        return None