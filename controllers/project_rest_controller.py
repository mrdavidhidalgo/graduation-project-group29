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
        
@router.get("/projects")
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
