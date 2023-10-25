import datetime
from fastapi import APIRouter, HTTPException, Header, Response, status

from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Annotated, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from daos.db_model.database import SessionLocal

from controllers import management_service_facade
from services import logs
LOGGER = logs.get_logger()

router = APIRouter()

class CreateProjectRequest(BaseModel):
    projectName : str
    startDate : str
    active : str
    details : str
    companyId : str
    
class ReadProjectRequest(BaseModel):    
    id : int
    projectName : str
    startDate : str
    active : str
    creationTime : str
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
async def create_project(request: CreateProjectRequest, db: Session = Depends(get_db)):
    #LOGGER.info("Peticion [%s] - [%s]", str(request.document), str(request.documentType))
    request2 = management_service_facade.CreateProjectRequest(project_name = request.projectName, start_date = request.startDate,\
    active = request.active, details= request.details,  company_id = request.companyId)
        
    try:
        management_service_facade.create_project(request = request2, db = db)
        return {"msg": "Project has been created"}
    except (management_service_facade.ProjectNameAlreadyExistError) as e:
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