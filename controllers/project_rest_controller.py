import datetime
from fastapi import APIRouter, HTTPException, Response

from fastapi import Depends
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal
from fastapi import APIRouter, HTTPException 

from fastapi import Depends
from typing import Optional
 
from controllers import commons
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal 

from controllers import management_service_facade
from services import logs
import datetime 

from controllers import management_service_facade, commons
from services import logs
LOGGER = logs.get_logger()

router = APIRouter()

class CreateProjectRequest(BaseModel):
    projectName : str
    startDate : str
    active : bool
    details : str
    
class ReadProjectRequest(BaseModel):    
    id : int
    projectName : str
    startDate : datetime.date
    active : int
    creationTime : datetime.datetime
    details : str
    companyId : str

class CreateMemberRequest(BaseModel):
    active : bool
    description : str
    personId : str
    profileId : str
    projectId : str

class CreatePerformanceEvaluationRequest(BaseModel):
    score : str
    details : str
    project_id : str
    person_id : str
    member_id : str
    
# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/projects")
async def create_project(request: CreateProjectRequest, token_data: commons.TokenData = Depends(commons.get_token_data), db: Session = Depends(get_db)):
    #LOGGER.info("Peticion [%s] - [%s]", str(request.document), str(request.documentType))
    
    start_date2 = string_to_date(start_date = request.startDate)
    
    request2 = management_service_facade.CreateProjectRequest(project_name = request.projectName, start_date = start_date2,\
    active = bool(request.active), details= request.details)
        
    try:
        management_service_facade.create_project(request = request2, person_id = token_data.person_id , db = db)
        return {"msg": "Project has been created"}
    except (management_service_facade.ProjectNameAlreadyExistError, management_service_facade.EmployeeDoesNotExistError) as e:
        raise HTTPException(status_code=400, detail=e.message)
        
@router.get("/projects/")
async def get_projects(company_id: str = None, db: Session = Depends(get_db)):
    project_list = management_service_facade.get_projects(db = db)
    if company_id:
        project_list = list(filter(lambda x: x.company_id==company_id,project_list))
    if project_list is not None:
        data=[]
        for project in project_list:
            data.append({'projectId': str(project.id),'name': str(project.project_name)})
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No projects found")
        
@router.get("/projects/myself")
async def get_projects_by_company(token_data: commons.TokenData = Depends(commons.get_token_data), db: Session = Depends(get_db)):
    project_list = management_service_facade.get_projects_by_company_id(person_id = token_data.person_id, db = db)

    if project_list is not None:
        data=[]
        for project in project_list:
            data.append({'id': str(project.id),'project_name': str(project.project_name), 
            'start_date': str(project.start_date), 'active': str(project.active),
            'creation_time': str(project.creation_time), 'details': str(project.details) })
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No projects found")


def string_to_date(start_date: str)->Optional[datetime.date]:
    
   
    date_format = '%Y-%m-%d'
    
    try:
        new_date = datetime.datetime.strptime(start_date, date_format).date()
    except:
        raise management_service_facade.InvalidDateError
    
    return new_date


 
class CreateProfileRequest(BaseModel):
    name : str = Field(min_length=6,max_length=200)
    description : str = Field(min_length=6,max_length=500)
    role :str= Field(min_length=1,max_length=200)
    experience_in_years : int = Field(gt=-1)
    technology :str= Field(min_length=2,max_length=200)
    category:str= Field(min_length=2,max_length=200)
    title:str= Field(min_length=2,max_length=200)
    project_id:str= Field(max_length=200)
    

# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/projects/profiles")
async def create_test(request: CreateProfileRequest,token_data: commons.TokenData = Depends(commons.get_token_data),
                      db: Session = Depends(get_db)):
    
    request = management_service_facade.CreateProfileRequest(**request.dict())
    
    try:
        management_service_facade.create_profile(request = request, db = db)
        return {"msg": "Profile has been created"}
    except (management_service_facade.ProfileNameAlreadyExistError):
        raise HTTPException(status_code=400, detail="Profile duplicated by name")

@router.get("/projects/profiles/{project_id}")
async def get_profiles_by_project_id(project_id: str, token_data: commons.TokenData = Depends(commons.get_token_data), db: Session = Depends(get_db)):
    profiles_list = management_service_facade.get_profiles_by_project_id(project_id=project_id, person_id = token_data.person_id, db = db)
    
    if profiles_list is not None:
        data=[]
        for profile in profiles_list:
            data.append({'projectId': str(project_id), 'name': str(profile.name)})
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No profiles found")


@router.post("/members")
async def create_member(request: CreateMemberRequest, token_data: commons.TokenData = Depends(commons.get_token_data), db: Session = Depends(get_db)):
    #LOGGER.info("Peticion [%s] - [%s]", str(request.document), str(request.documentType))
    request2 = management_service_facade.CreateMemberRequest(active = bool(request.active), description= request.description,\
    person_document=request.personId, profile_id = request.profileId, project_id= request.projectId)
        
    try:
        management_service_facade.create_member(request = request2, person_id = token_data.person_id, db = db)
        return {"msg": "Member has been created"}
    except (management_service_facade.ProjectMemberAlreadyExistError, management_service_facade.EmployeeDoesNotExistError) as e:
        LOGGER.info("No se pudo asignar [%s]", str(e.message))
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/projects/members/{project_id}")
async def get_members_by_project_id(project_id: str, token_data: commons.TokenData = Depends(commons.get_token_data), 
    db: Session = Depends(get_db)):
    member_list = management_service_facade.get_members_by_project_id(project_id=project_id, person_id = token_data.person_id, db = db)
        
    if member_list is not None:
        data=[]
        for member in member_list:
            data.append({'id': str(member.id), 'name': str(member.member_name), 'profile': str(member.profile),
            'active': str(member.active), 'performance': "" ,'description': str(member.description), 'person_id': str(member.person_id), 'project_id': str(project_id)
            })
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No members found")

@router.get("/projects/{project_id}")
async def get_project_by_id(project_id: str, token_data: commons.TokenData = Depends(commons.get_token_data), 
    db: Session = Depends(get_db)):
    project = management_service_facade.get_project_by_id(project_id=project_id, person_id = token_data.person_id, db = db)
    
    if project is not None:
        data=[]
        data.append({'id': str(project.id), 'project_name': str(project.project_name), 'start_date': str(project.start_date),
            'active': str(project.active), 'creation_time': str(project.creation_time) ,'details': str(project.details),
             'company_id': str(project.company_id)
            })
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No projects found")
        

@router.post("/evaluations")
async def create_evaluation(request: CreatePerformanceEvaluationRequest, token_data: commons.TokenData = Depends(commons.get_token_data),
 db: Session = Depends(get_db)):
    #LOGGER.info("Peticion [%s] - [%s]", str(request.document), str(request.documentType))
    request2 = management_service_facade.CreateEvaluationRequest(score = request.score, details= request.details,\
    project_id= request.project_id, person_document=request.person_id, member_id = request.member_id )
        
    try:
        management_service_facade.create_evaluation(request = request2, person_id = token_data.person_id, db = db)
        return {"msg": "Performance evaluation has been created"}
    except (management_service_facade.ProjectMemberHasEvaluationError, management_service_facade.EmployeeDoesNotExistError,
    management_service_facade.ProjectMemberNotExistsError ) as e:
        LOGGER.info("No se pudo crear [%s]", str(e.message))
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/evaluations/{project_id}")
async def get_evaluations_by_project_id(project_id: str, token_data: commons.TokenData = Depends(commons.get_token_data), 
    db: Session = Depends(get_db)):
    evaluations_list = management_service_facade.get_evaluations_by_project_id(project_id=project_id, person_id = token_data.person_id, db = db)
        
    if evaluations_list is not None:
        data=[]
        for evaluation in evaluations_list:
            data.append({'id': str(evaluation.id), 'creation_date': str(evaluation.creation_date), 'score': str(evaluation.score),
            'details': str(evaluation.details), 'project_id': str(project_id), 'person_id': str(evaluation.person_id), 
            'member_id': str(evaluation.member_id),'person_name': str(evaluation.person_name)
            })
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No evaluations found")
        
@router.get("/evaluations/{project_id}/{member_id}")
async def get_evaluations_by_person_id(project_id: str, member_id: str, token_data: commons.TokenData = Depends(commons.get_token_data), 
    db: Session = Depends(get_db)):
    evaluations_list = management_service_facade.get_evaluations_by_person_id(project_id=project_id, person_id = token_data.person_id, 
    member_id=member_id ,db = db)
        
    if evaluations_list is not None:
        data=[]
        for evaluation in evaluations_list:
            data.append({'id': str(evaluation.id), 'creation_date': str(evaluation.creation_date), 'score': str(evaluation.score),
            'details': str(evaluation.details), 'project_id': str(project_id), 'person_id': str(evaluation.person_id), 
            'member_id': str(evaluation.member_id),'person_name': str(evaluation.person_name)
            })
        return data
    else:
        LOGGER.info("Return 404 error")
        raise HTTPException(status_code=404, detail="No evaluations found for member")