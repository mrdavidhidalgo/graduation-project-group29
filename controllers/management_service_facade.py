
import datetime
import decimal
import string
from typing import List, Optional
from sqlalchemy.orm import Session
from services.company import company_service
from services.employee import employee_service
from services.interview import interview_service
from services.interview.contracts import interview_repository
from services.interview.model import interview_model
from services.project.contracts import project_repository, member_repository
from services.test import test_service
from services.user import user_service
import enum
from services.person import person_service
from services.professional import professional_service
from typing import List,Set
from services.technology import technology_service
from services.ability import ability_service
from daos import db_user_repository,db_test_repository, db_person_repository, db_professional_repository,\
db_employee_repository, db_company_repository, db_project_repository, db_technology_repository,\
db_ability_repository, db_profile_repository, db_member_repository, db_performance_evaluation_repository,db_interview_repository

from services.project import project_service, profile_service, member_service, performance_evaluation_service
from pydantic import BaseModel
from services.professional.model import professional_model
from services.person.model import person_model
from services.project.model import project_model, profile_model, member_model, performance_evaluation_model

from services.technology.model import technology_model
from services.commons import base

class DateRangeInvalidError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = f"The Range of dates is invalid"
        super().__init__(self.message)

class InvalidDateError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = f"Incorrect data format, should be AAAA-MM-DD"
        super().__init__(self.message)
        
import jwt
class LoginResponse(BaseModel):
    token: str
    username: str
    role: str
    person_id:int
    
class AuthenticationResponse(BaseModel):
    new_token: str
    username: str
    role:str
    exp:int
    person_id:int
    
UserLoginValidationError = user_service.UserLoginValidationError

UserLoginError = user_service.UserLoginError

UserNameAlreadyExistError = user_service.UserNameAlreadyExistError

PersonDocumentAlreadyExistError = person_service.PersonDocumentAlreadyExistError

UserNameDoesNotExistError = user_service.UserNameDoesNotExistError

ProfessionalDoesNotExistError = professional_service.ProfessionalDoesNotExistError

ProfessionalAlreadyExistError = professional_service.ProfessionalAlreadyExistError

CompanyTaxprayerAlreadyExistError = company_service.CompanyTaxprayerAlreadyExistError

ProjectNameAlreadyExistError = project_service.ProjectNameAlreadyExistError

EmployeeDoesNotExistError = employee_service.EmployeeDoesNotExistError

TestNameAlreadyExistError = test_service.TestNameAlreadyExistError


TechnologyAlreadyExistError = technology_service.TechnologyAlreadyExistError

AbilityAlreadyExistError = ability_service.AbilityAlreadyExistError

ProfileNameAlreadyExistError = profile_service.ProfileNameAlreadyExistError

ProfessionalSearchError = professional_service.ProfessionalSearchError

ProjectMemberAlreadyExistError = member_service.ProjectMemberAlreadyExistError

ProjectMemberNotExistsError = member_service.ProjectMemberNotExistsError

ProjectMemberHasEvaluationError = performance_evaluation_service.ProjectMemberHasEvaluationError

ProjectHasNotEvaluationsError = performance_evaluation_service.ProjectHasNotEvaluationsError
InterviewAlreadyExistError = interview_service.InterviewAlreadyExistError

#LOGGER = user_service.LOGGER
from services import logs
LOGGER = logs.get_logger()

    
class LoginRequest(BaseModel):
    username: str
    password: str
    
class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str
    person: int

class CreateCandidateRequest(BaseModel):
    document: str
    document_type: base.DocumentType
    first_name: str
    last_name: str
    phone_number: str
    username: str
    password: str
    birth_date: str
    age: int
    origin_country: base.Country
    residence_country: base.Country
    residence_city: str
    address: str
    
class CreateCandidateLaboralInfoRequest(BaseModel):
    person_id : str
    position: str
    company_name: str
    company_country: base.Country
    company_address: str
    company_phone: str
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str

class CreateCompanyRequest(BaseModel):
    document: str
    document_type: str
    first_name: str
    last_name: str
    username: str
    password: str
    taxpayer_id: str
    name: str
    country: str
    city: str
    years: str
    address: str
    phone_number: str
    profile: str
    position: str
    
class CreateProjectRequest(BaseModel):
    project_name : str
    start_date : datetime.date
    active : bool
    details : str


class Status(enum.Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"

class CreateTestRequest(BaseModel):
    name : str
    technology : str
    duration_minutes : int
    status : Status
    start_date : datetime.date 
    end_date: datetime.date
    description : str 


class Status(enum.Enum):
    SCHEDULED = "SCHEDULED"
    DONE = "DONE"
    CANCELLED ="CANCELLED"

class CreateInterviewRequest(BaseModel):
    candidate_document : str 
    project_id : str
    meet_url : str
    status : Status
    profile_id : str
    start_timestamp : datetime.datetime 
    duration_minutes: int

class CreateTestReponse(BaseModel):
    name : str
    technology : str
    duration_minutes : int
    status : str
    start_date : datetime.date 
    end_date: datetime.date
    description : str 

class RegisterTestResultRequest(BaseModel):
    test_name : str 
    candidate_document: str
    observation :str|None
    points : int 

class CreateTechnologyRequest(BaseModel):
    technology_name : str
    details : str
    category : base.TechnologyCategory
    
class ReadTechnologyRequest(BaseModel):    
    id : int
    technology_name : str
    details : str
    category : base.TechnologyCategory
    
class AbilityInterviewRequest(BaseModel):
    ability_id: int
    qualification: int

class LoadInterviewRequest(BaseModel):
    candidate_document : str
    project_id : str
    profile_id : str
    date : datetime.date
    recording_file: Optional[str]
    test_file : Optional[str]
    observation: str
    abilities: List[AbilityInterviewRequest]
  
######################################################################################################################################
#                                                           USER                                                                     #
######################################################################################################################################

def myself(token:str)->AuthenticationResponse:

    new_token, map = user_service.myself(token)
        
    return AuthenticationResponse(new_token = new_token, username=map["user"],
                                  role=map["role"],exp=map["exp"],person_id=map["person_id"]) 

def login(login_request: LoginRequest, db: Session)->LoginResponse:
    
    user_repository = db_user_repository.DBUserRepository(db = db)
    
    token,data = user_service.login_user(user_repository=user_repository, username=login_request.username, password=login_request.password)
    
    return LoginResponse(token = token, username=login_request.username,role=data["role"],person_id=data["person_id"]) 

def create_user(request: CreateUserRequest, db: Session)->None:
    
    user_repository = db_user_repository.DBUserRepository(db = db)
    
    user_service.create_user(user_repository=user_repository, username=request.username, password=request.password, role=request.role, person = request.person)
    


######################################################################################################################################
#                                                       CANDIDATE                                                                    #
######################################################################################################################################


class CreateCandidateAcademicInfoRequest(BaseModel):
    person_id : str
    title : str
    institution : str
    country : base.Country
    start_date : datetime.datetime
    end_date : Optional[datetime.datetime]
    description : str
    
class CreateCandidateTechnicalRoleInfoRequest(BaseModel):
    person_id : str
    role: str
    experience_years: int
    description : str
    
class CreateCandidateTechnologyInfoRequest(BaseModel):
    person_id : str
    name: str
    experience_years: int
    level: int
    description : str
    
class CandidateSearchRequest(BaseModel):
    role_filter: str
    role: str
    role_experience: str
    technologies: list = []
    abilities: list = []
    title_filter: str
    title: str
    title_experience: str

def create_candidate(request: CreateCandidateRequest, db: Session)->None:

    LOGGER.info("Starting Create candidate with username [%s]", request.username)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    user_repository = db_user_repository.DBUserRepository(db = db)
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    new_request = person_service.CreateCandidateRequest.model_validate(request.model_dump())
    
    person_service.create_candidate(request=new_request, 
                                       person_repository=person_repository, 
                                       user_repository=user_repository,
                                       professional_repository=professional_repository)

def get_candidates(db: Session)->List[person_service.person_model.Person]:
    LOGGER.info("Listing all candidates")
    person_repository = db_person_repository.DBPersonRepository(db = db)
    professional_list = person_service.get_all(person_repository=person_repository)
    
    if professional_list is None:
        LOGGER.info("Empty List in facade")
        return None
    else:
        LOGGER.info("List with data in facade")
        return professional_list
    
def add_candidate_academic_info(request: CreateCandidateAcademicInfoRequest, db: Session)->None:
    
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    professional_service.add_academic_info(academic_info=professional_model.ProfessionalAcademicInfo.model_validate(request.model_dump()), 
                                           professional_repository = professional_repository)
    
def add_candidate_laboral_info(request: CreateCandidateLaboralInfoRequest, db: Session)->None:
    
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    professional_service.add_laboral_info(laboral_info=professional_model.ProfessionalLaboralInfo.model_validate(request.model_dump()), 
                                           professional_repository = professional_repository)
    
def add_candidate_technical_role_info(request: CreateCandidateTechnicalRoleInfoRequest, db: Session)->None:
    
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    professional_service.add_technical_role(technical_role=professional_model.ProfessionalTechnicalRole.model_validate(request.model_dump()), 
                                           professional_repository = professional_repository)
    
def add_candidate_technology_info(request: CreateCandidateTechnologyInfoRequest, db: Session)->None:
    
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    
    professional_service.add_technology_info(technology_info=professional_model.ProfessionalTechnologyInfo.model_validate(request.model_dump()), 
                                           professional_repository = professional_repository)

def search_for_candidates(request: CandidateSearchRequest, db: Session)->Optional[List[professional_model.ProfessionalSearchResult]]:
    LOGGER.info("Listing all candidates")
    professional_repository = db_professional_repository.DBProfessionalRepository(db = db)
    professional_list = professional_service.search_for_candidates(request, professional_repository=professional_repository)
    
    if professional_list is None:
        LOGGER.info("Empty List in facade")
        return None
    else:
        LOGGER.info("List with data in facade")
        return professional_list

######################################################################################################################################
#                                                       COMPANIES                                                                    #
######################################################################################################################################

def create_company(request: CreateCompanyRequest, db: Session)->None:

    LOGGER.info("Starting Create company with username [%s]", request.name)
    company_repository = db_company_repository.DBCompanyRepository(db = db)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    user_repository = db_user_repository.DBUserRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    
    new_company = company_service.CreateCompanyRequest.model_validate(request.model_dump())
    
    company_service.create_company(request=new_company, 
                                       person_repository=person_repository, 
                                       user_repository=user_repository,
                                       company_repository = company_repository,
                                       employee_repository=employee_repository)

def get_companies(db: Session)->Optional[List[company_service.company_model.Company]]:
    LOGGER.info("Listing all companies")
    company_repository = db_company_repository.DBCompanyRepository(db = db)
    company_list = company_service.get_all(company_repository=company_repository)
    
    if company_list is None:
        LOGGER.info("Empty List in facade")
        return None
    else:
        LOGGER.info("List with data in facade")
        return company_list
    
    
def get_company_by_person_id(person_id: str, db: Session)->Optional[List[company_service.company_model.Company]]:
    LOGGER.info("Listing all companies for person")
    company_repository = db_company_repository.DBCompanyRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    user_repository = db_user_repository.DBUserRepository(db = db)
    company = company_service.get_by_person_Id(person_id= person_id,\
    company_repository=company_repository, employee_repository = employee_repository,\
    person_repository = person_repository, user_repository=user_repository)
    
    if company is None:
        LOGGER.info("Empty Company List in facade")
        return None
    else:
        LOGGER.info("Company List with data in facade")
        return company
    

######################################################################################################################################
#                                                         TEST                                                                       #
######################################################################################################################################

def create_test(request: CreateTestRequest, db: Session)->None:
    
    test_repository = db_test_repository.DBTestRepository(db = db)
    
    test_service.create_test(**request.copy(exclude={"status"}).dict(),status=request.status.name, test_repository=test_repository)

def get_tests(db: Session)->List[CreateTestReponse]:

    test_repository = db_test_repository.DBTestRepository(db = db)
    
    result = test_service.get_tests(test_repository=test_repository)

    return [] if result is None or len(result)==0 else [CreateTestReponse(**x.dict()) for x in result]
    
def register_result_tests(request: List[RegisterTestResultRequest], db: Session)->None:
    
    test_repository = db_test_repository.DBTestRepository(db = db)
    
    results = [(r.test_name,r.candidate_document, r.observation,r.points ) for r in request]
    test_service.register_result_tests(results, test_repository=test_repository)
            
        
        
######################################################################################################################################
#                                                           PROJECT                                                                  #
######################################################################################################################################

def create_project(request: CreateProjectRequest, person_id: str, db: Session)->None:

    LOGGER.info("Starting Create project with name [%s]", request.project_name)
    project_repository = db_project_repository.DBProjectRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    
    new_project = project_service.CreateProjectRequest.model_validate(request.model_dump())
    
    project_service.create_project(request=new_project, person_id= person_id, 
                                       project_repository=project_repository, employee_repository = employee_repository)

def get_projects(db: Session)->Optional[List[project_service.project_model.ProjectRead]]:
    LOGGER.info("Listing all projects")

    project_list = project_service.get_all(project_repository=db_project_repository.DBProjectRepository(db = db))
    
    if project_list is None:
        LOGGER.info("Empty Project List in facade")
        return None
    else:
        LOGGER.info("Project List with data in facade")
        return project_list


def get_projects_by_company_id(person_id: str, db: Session)->Optional[List[project_service.project_model.ProjectRead]]:
    LOGGER.info("Listing all projects for company")
    project_repository = db_project_repository.DBProjectRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    project_list = project_service.get_projects_by_company_id(person_id= person_id,\
     project_repository=project_repository, employee_repository = employee_repository)
    
    if project_list is None:
        LOGGER.info("Empty Company Project List in facade")
        return None
    else:
        LOGGER.info("Company Project List with data in facade")
        return project_list


def get_project_by_id(project_id: str, person_id: str, db: Session)->Optional[project_service.project_model.ProjectRead]:
    LOGGER.info("Serach project by ID")
    project_repository = db_project_repository.DBProjectRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    project_info = project_service.get_by_project_id(project_id= project_id, person_id= person_id,\
    project_repository=project_repository, employee_repository = employee_repository)
    
    return project_info

######################################################################################################################################
#                                                      TECHNOLOGY                                                                    #
######################################################################################################################################


def get_technologies(db: Session)->Optional[List[technology_service.technology_model.TechnologyRead]]:
    LOGGER.info("Listing all technologies")
    technology_repository = db_technology_repository.DBTechnologyRepository(db = db)
    technology_list = technology_service.get_all(technology_repository=technology_repository)
    
    if technology_list is None:
        LOGGER.info("Empty Technology List in facade")
        return None
    else:
        LOGGER.info("Technology List with data in facade")
        return technology_list
        

######################################################################################################################################
#                                                      ABILITY                                                                       #
######################################################################################################################################

def get_abilities(db: Session)->Optional[List[ability_service.ability_model.AbilityRead]]:
    LOGGER.info("Listing all abilities")
    ability_repository = db_ability_repository.DBAbilityRepository(db = db)
    ability_list = ability_service.get_all(ability_repository=ability_repository)
    
    if ability_list is None:
        LOGGER.info("Empty Ability List in facade")
        return None
    else:
        LOGGER.info("Ability List with data in facade")
        return ability_list

######################################################################################################################################
#                                                           PROFILE                                                                  #
######################################################################################################################################

 
class CreateProfileRequest(BaseModel):
    name : str
    description : str 
    role :str
    experience_in_years : int
    technology :str
    category:str
    title:str
    project_id:str

def create_profile(request: CreateProfileRequest, db: Session)->None:

    LOGGER.info("Starting Create profile with name [%s]", request.name)
    
    profile_service.create_profile(**request.model_dump(),
                                       profile_repository=db_profile_repository.DBProfileRepository(db = db))


def get_profiles_by_project_id(project_id: str, person_id: str, db: Session)->Optional[List[profile_model.Profile]]:
    LOGGER.info("Listing all profiles for project [%s]", str(project_id))
    profile_repository = db_profile_repository.DBProfileRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    profile_list = profile_service.get_profiles_by_project_id(project_id=project_id, person_id= person_id,\
     profile_repository=profile_repository, employee_repository = employee_repository)
    
    if profile_list is None:
        LOGGER.info("Empty Profiles Project List in facade")
        return None
    else:
        LOGGER.info("Profiles Project List with data in facade")
        return profile_list
    
class ProfileAndProject(BaseModel):
    project_id : str
    project_name : str
    profile_names : Set[str]
    
def get_profiles_and_projects( db: Session)->List[ProfileAndProject]:


    project_repo = db_project_repository.DBProjectRepository(db = db)
    member_repo= db_member_repository.DBMemberRepository(db = db)
    return member_service.get_profile_and_projects(member_repository=member_repo,project_repository=project_repo)


######################################################################################################################################
#                                                           MEMBER                                                                   #
######################################################################################################################################

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
        
def create_member(request: CreateMemberRequest, person_id: str, db: Session)->None:

    LOGGER.info("Starting added member to project[%s]", str(request.project_id))
   
    member_repository = db_member_repository.DBMemberRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    
    new_member = member_service.CreateMemberRequest.model_validate(request.model_dump())
    
    member_service.create_member(request=new_member, person_id= person_id, 
                                       member_repository=member_repository, employee_repository = employee_repository)
    
def get_members_by_project_id(project_id: str, person_id: str,db: Session)->Optional[List[ProjectMemberRequest]]:
    LOGGER.info("Listing all members for project [%s]", str(project_id))

    member_repository = db_member_repository.DBMemberRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    project_repository = db_project_repository.DBProjectRepository(db = db)
    member_list = member_service.get_members_by_project_id(project_id=project_id, person_id= person_id,\
     member_repository=member_repository, employee_repository = employee_repository, 
     person_repository=person_repository)
    
    if member_list is None:
        LOGGER.info("Empty members Project List in facade")
        return None
    else:
        LOGGER.info("Member Project List with data in facade")
        return member_list
        
              
######################################################################################################################################
#                                                           CANDIDATES                                                               #
######################################################################################################################################

class ProfessionalInfo(BaseModel):
    info: person_model.Person
    professional_data :professional_model.ProfessionalFullInfo

def get_full_info(person_id: str, db: Session)->ProfessionalInfo:

    person_repository = db_person_repository.DBPersonRepository(db=db)
    professional_repository = db_professional_repository.DBProfessionalRepository(db =db)
    
    person = person_service.find_by_person_id(person_id=person_id, person_repository=person_repository)
    
    professional_full_info = professional_service.get_full_info(person_id=person_id, professional_repository=professional_repository)
    
    return ProfessionalInfo(info=person, professional_data = professional_full_info)




def get_candidates_without_interviews(db:Session)->List[professional_model.ProfessionalReadModel]:
    return professional_service.get_candidates_without_interviews(db_professional_repository.DBProfessionalRepository(db=db))


def load_interview(request: LoadInterviewRequest, db:Session)->None:
    
    interview_info = interview_model.LoadInterviewInfo.model_validate(request.model_dump())
    
    return interview_service.load_interview(interview_info=interview_info, interview_repository=db_interview_repository.DBInterviewRepository(db=db))


######################################################################################################################################
#                                                           PERFORMACE EVALUATION                                                    #
######################################################################################################################################

class CreateEvaluationRequest(BaseModel):
    score : str
    details : str
    project_id : str
    person_document : str
    member_id : str

class PerformanceEvaluationResponse(BaseModel):
    id : int
    creation_date: str
    score : str
    details : str
    project_id : str
    person_id : str
    member_id : str
    person_name : str
    
def create_evaluation(request: CreateEvaluationRequest, person_id: str, db: Session)->None:

    LOGGER.info("Starting create evaluation to project[%s]", str(request.project_id))
   
    performance_evaluation_repository = db_performance_evaluation_repository.DBPerformanceEvaluationRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    member_repository = db_member_repository.DBMemberRepository(db = db)
    
    new_evaluation = performance_evaluation_service.CreateEvaluationRequest.model_validate(request.model_dump())
    
    performance_evaluation_service.create_evaluation(request=new_evaluation, person_id= person_id, 
        performance_evaluation_repository=performance_evaluation_repository, employee_repository = employee_repository,
        person_repository=person_repository, member_repository=member_repository)
    
def get_evaluations_by_project_id(project_id: str, person_id: str,db: Session)->Optional[List[PerformanceEvaluationResponse]]:
    LOGGER.info("Listing all evaluations for project [%s]", str(project_id))

    performance_evaluation_repository = db_performance_evaluation_repository.DBPerformanceEvaluationRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    
  
    evaluation_list = performance_evaluation_service.get_evaluations_by_project_id(project_id=project_id, person_id= person_id,
    performance_evaluation_repository=performance_evaluation_repository, employee_repository = employee_repository,
    person_repository=person_repository)
    
    if evaluation_list is None:
        LOGGER.info("There are not evaluations List in facade")
        return None
    else:
        LOGGER.info("Evaluations List with data in facade")
        return evaluation_list
        

def get_evaluations_by_person_id(project_id: str, person_id: str, member_id: str, db: Session)->Optional[List[PerformanceEvaluationResponse]]:
    LOGGER.info("Listing all evaluations for Mimembro [%s]", str(member_id))

    performance_evaluation_repository = db_performance_evaluation_repository.DBPerformanceEvaluationRepository(db = db)
    employee_repository = db_employee_repository.DBEmployeeRepository(db = db)
    person_repository = db_person_repository.DBPersonRepository(db = db)
    
  
    evaluation_list = performance_evaluation_service.get_evaluations_by_member_id(project_id=project_id, person_id= person_id, 
    member_id = member_id, performance_evaluation_repository=performance_evaluation_repository, employee_repository = employee_repository,
    person_repository=person_repository)
    
    if evaluation_list is None:
        LOGGER.info("There are not evaluations for memeber in facade")
        return None
    else:
        LOGGER.info("Evaluation data in facade")
        return evaluation_list

######################################################################################################################################
#                                                      Interviews                                                                    #
######################################################################################################################################

def create_inverview(request: CreateInterviewRequest, db: Session)->None:
    
    interview_repo = db_interview_repository.DBInterviewRepository(db = db)
    
    interview_service.create_interview(**request.copy(exclude={"status"}).dict(),status=request.status.name, 
                                       interview_repository=interview_repo)


def get_intervies(candidate_document: str|None, db: Session)->None:
    
    interview_repo = db_interview_repository.DBInterviewRepository(db = db)
    
    return interview_service.get_interviews(candidate_document, 
                                       interview_repository=interview_repo)



class AbilityInterviewInfo(BaseModel):
    ability_id: int
    qualification: int

class LoadInterviewInfo(BaseModel):
    id:int|None=None 
    candidate_document : str 
    project_id : str
    profile_id: str
    date: datetime.date
    recording_file: str | None
    test_file : str | None
    observation: str
    abilities: List[AbilityInterviewInfo]
    
    @property
    def qualification(self) -> decimal.Decimal | None:
        l=[a.qualification for a in self.abilities]
        r= decimal.Decimal(sum(l)/len(l)).quantize(decimal.Decimal('0.00'))
        return r

def find_interview_results(db: Session)->List[LoadInterviewInfo]:
    
    result =  interview_service.find_interview_results(db_interview_repository.DBInterviewRepository(db)) 

    return [LoadInterviewInfo(**i.dict()) for i in result]


def find_interview_result(id:int,db: Session)-> LoadInterviewInfo | None:
    
    result =  interview_service.find_interview_result(id,db_interview_repository.DBInterviewRepository(db)) 
    return LoadInterviewInfo(**result.dict())



class PendingInterviewInfo(BaseModel):
    candidate_document : str 
    project_id : str
    project_name: str
    profile_id: str
    date: datetime.datetime

def get_pending_interviews(db: Session)->None:
    
    interview_repo = db_interview_repository.DBInterviewRepository(db = db)
    person_repo = db_person_repository.DBPersonRepository(db = db)
    project_repo=db_project_repository.DBProjectRepository(db = db)

    return interview_service.get_pending_interviews(interview_repository=interview_repo, 
                                                    person_repository=person_repo,
                                                    project_repository=project_repo
                                                    )
                            