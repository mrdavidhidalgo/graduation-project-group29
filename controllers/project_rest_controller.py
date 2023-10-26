import datetime
from fastapi import APIRouter, HTTPException, Header, Response, status

from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Annotated, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal

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
async def get_projects(response: Response, db: Session = Depends(get_db)):
    project_list = management_service_facade.get_projects(db = db)
    
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