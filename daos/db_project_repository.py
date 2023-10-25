from typing import Optional, List
from .db_model import db_model as models

from services.project.contracts import project_repository

from sqlalchemy.orm import Session

from services.project.model import project_model
from services import logs
LOGGER = logs.get_logger()

class DBProjectRepository(project_repository.ProjectRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_project_name(self, project_name: str, company_id: int)-> project_model.ProjectRead:
        project = self.db.query(models.Project).filter(models.Project.project_name == project_name, \
        models.Project.company_id == company_id).first()
       
        return None if project is None else project_model.ProjectRead(id = project.id, project_name=project_name,\
         start_date = str(project.start_date), active= project.active, creation_time = str(project.creation_time), details = project.details,\
          company_id = company_id)
          
    def get_by_project_id(self, project_id: str)-> project_model.ProjectRead:
        project = self.db.query(models.Project).filter(models.Project.project_id == project_id).first()
       
        return None if project is None else project_model.ProjectRead(id = project_id, project_name=project.project_name,\
         start_date = project.start_date, active= project.active, creation_time = project.creation_time, details = project.details,\
          company_id = project.company_id)
    
    def get_all(self)-> Optional[List[project_model.ProjectRead]]:
        
        projects = self.db.query(models.Project).all()
        if len(projects) ==0:
            LOGGER.info("There are not project records")
            None
        else:
            LOGGER.info("Sending project list")
            return [project_model.ProjectRead(id = project.id, project_name=project.project_name,\
            start_date = str(project.start_date), active= project.active, creation_time = str(project.creation_time),\
            details = project.details, company_id = project.company_id)   for project in projects]
                
    def save(self, project: project_model.ProjectCreate)-> None:
        new_project = models.Project(
            project_name = project.project_name,
            start_date = project.start_date,
            active = project.active,
            details = project.details,
            company_id = project.company_id
        )
        
        self.db.add(new_project)
        self.db.commit()

    def delete_project(self, project_id: int)-> Optional[int]:
        project = self.db.query(models.Project).filter(models.Project.id == project_id).delete()
        self.db.commit()
        return project
        