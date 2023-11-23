from datetime import timedelta
import datetime
from typing import List, Optional

from services.project.contracts import performance_evaluation_repository,\
    project_repository, profile_repository, member_repository
from services.person.contracts import person_repository
from services.employee.contracts import employee_repository
from services.employee import employee_service
from services.project import member_service
from services.project.model import member_model, performance_evaluation_model
from pydantic import BaseModel,Field


import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class ProjectMemberHasEvaluationError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Project Member  already has a performance evaluation"
        super().__init__(self.message)

class ProjectHasNotEvaluationsError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Project has not performance evaluations"
        super().__init__(self.message)   
        
class CreateEvaluationRequest(BaseModel):
    score : str 
    details : str = Field(min_length=6,max_length=500)
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
    
def create_evaluation(request : CreateEvaluationRequest, person_id: str, performance_evaluation_repository: performance_evaluation_repository.PerformanceEvaluationRepository,\
employee_repository: employee_repository.EmployeeRepository, person_repository: person_repository.PersonRepository,\
    member_repository: member_repository.MemberRepository)-> None:
    
    employee_project = employee_service.get_by_person_id(employee_repository, person_id = person_id)
    if employee_project is None:
        raise employee_service.EmployeeDoesNotExistError()
    
    member_project = member_repository.get_by_member_id(request.person_document, request.project_id)
    
    if member_project is None:
        raise member_service.ProjectMemberNotExistsError()
    
    persisted_evaluation = performance_evaluation_repository.get_by_person_id(person_id = request.person_document, project_id = request.project_id)
    #LOGGER.info("Value of persisted_member [%s] in service", str(persisted_member))
    
    if persisted_evaluation is not None:
        raise ProjectMemberHasEvaluationError()
    
    
    performance_evaluation_repository.save(
        evaluation=performance_evaluation_model.PerformanceEvaluationCreate(
            score = request.score,
            details = request.details,
            project_id = request.project_id,
            person_id = request.person_document,
            member_id = request.member_id
            )
        )

def get_evaluations_by_project_id(project_id: str, person_id: str, performance_evaluation_repository: performance_evaluation_repository.PerformanceEvaluationRepository,
    employee_repository: employee_repository.EmployeeRepository, person_repository: person_repository.PersonRepository
    )->Optional[List]:
    LOGGER.info("Search for members by project [%s] in service", str(project_id))
    
    employee_project = employee_service.get_by_person_id(employee_repository, person_id = person_id)
    if employee_project is None:
        raise employee_service.EmployeeDoesNotExistError()
    
    LOGGER.info("sending  to evaluation repo [%s]", project_id)    
    
    evaluations = performance_evaluation_repository.get_by_project_id(project_id=project_id)    
    
    if (evaluations is None) or len(evaluations) < 1:
        LOGGER.info("Empty List evaluations in service")
        return None
    
    evaluations_project_list = []
    evaluation_response = PerformanceEvaluationResponse
    for evaluation in evaluations:
        person = person_repository.get_by_document(evaluation.person_id)
        evaluation_response = PerformanceEvaluationResponse(id  = str(evaluation.id), 
            creation_date= str(evaluation.creation_date), score =str(evaluation.score),
            details= str(evaluation.details), project_id = str(project_id),
            person_id = str(evaluation.person_id), member_id = str(evaluation.member_id), 
            person_name = person.first_name + " " + person.last_name)
            
        evaluations_project_list.append(evaluation_response)
    
    LOGGER.info("Evaluation List with data in service")
    return evaluations_project_list