
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

@pytest.mark.unittests
def test_create_candidate_successfully():
    from services.person import person_service as subject
    
    candidate_request = subject.CreateCandidateRequest(document= "2343523",document_type= "CC",first_name= "Jorge",last_name= "Lopez",
	phone_number= "64345678",username= "jlopes453@gmail.com",password= "DHSc532XSC..",birth_date= "1989-12-11", age= "34",
        origin_country= "CO",residence_country= "AR", residence_city= "Belgrano",address="Arroyito 14-11")
    
    candidate=subject.create_candidate(request=candidate_request, person_repository=MockPerson(), user_repository=MockUser(),
    professional_repository=MockProfessional())
    assert candidate is None

@pytest.mark.unittests
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
        return self.person_with_params
        
    def delete_user(self, username: str)-> Optional[int]:
        return 1
         
class MockProfessional(professional_repository.ProfessionalRepository):
   
    def __init__(self,professional_by_id: professional_model.ProfessionalCreateModel=None,professional_with_params:professional_model.ProfessionalCreateModel=None)->None:
       self.by_id=professional_by_id
       self.professional_with_params=professional_with_params
    
    def get_by_person_id(self, person_id: str)-> Optional[professional_model.ProfessionalReadModel]:
        return None
    
    def get_full_info(self, professional_id: int)-> List[professional_model.ProfessionalFullInfo]:
        return []
    
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
    
    def delete_professional(self, person_id: int)-> Optional[int]:
        return 1
        
    def search_for_candidates(self, role_filter: str, role: str, role_experience: str,\
     technologies: list, abilities: list , title_filter: str, title: str, title_experience: str)->Optional[List[professional_model.ProfessionalSearchResult]]:
        return None if (len(role)==0) & (len(title)==0) & (len(technologies)==0)\
            else [professional_model.ProfessionalSearchResult(person_id = 1,
                first_name= "Andres",
                last_name="Gomez", 
                age = "30",
                roles = [{'roles': 'PROGRAMADOR[5]'}],
                titles = [{'title': 'ING SISTEMAS[8]'}],
                technologies= [{'name': 'JAVA[5]'}],
                abilities= {'name': 'Ninguna'},
                score= "9"
        )]
            
    def get_candidates_without_interviews(self)->List[professional_model.ProfessionalReadModel]:
        ...
        
    def load_interview(self, interview_info: professional_model.LoadInterviewInfo)->None:
        ...