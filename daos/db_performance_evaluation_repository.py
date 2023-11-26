from typing import Optional, List
from .db_model import db_model as models
from sqlalchemy import text, select
from services.project.contracts import performance_evaluation_repository

from sqlalchemy.orm import Session

from services.project.model import performance_evaluation_model
from services import logs
LOGGER = logs.get_logger()

class DBPerformanceEvaluationRepository(performance_evaluation_repository.PerformanceEvaluationRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
    
    def get_by_person_id(self, person_id: str, project_id: str)->Optional[performance_evaluation_model.PerformanceEvaluationRead]:
        evaluations = self.db.query(models.PerformaceEvaluation).filter(models.PerformaceEvaluation.person_id == person_id).filter(models.ProjectMember.project_id == project_id).all()
        count = len(evaluations)
        print(count)
        
        return None if count==0 else [performance_evaluation_model.PerformanceEvaluationRead(id = str(evaluation.id), score=str(evaluation.score),
            details = evaluation.details, creation_date= str(evaluation.creation_date) ,project_id = str(evaluation.project_id),
            person_id = str(evaluation.person_id), member_id= str(evaluation.member_id)) for evaluation in evaluations]
    
                
    def save(self, evaluation:performance_evaluation_model.PerformanceEvaluationCreate)-> None:
        new_evaluation = models.PerformaceEvaluation(
            score = evaluation.score,
            details = evaluation.details,
            project_id = evaluation.project_id,
            person_id = evaluation.person_id,
            member_id = evaluation.member_id
            )
        self.db.add(new_evaluation)
        self.db.commit()
        
    def get_by_project_id(self, project_id: str)->Optional[List[performance_evaluation_model.PerformanceEvaluationRead]]:
        evaluations = self.db.query(models.PerformaceEvaluation).filter(models.PerformaceEvaluation.project_id == project_id).all()
        LOGGER.info("Filter in repository: [%s]-[%s]", project_id, str(evaluations))
        
        return None if evaluations is None else [performance_evaluation_model.PerformanceEvaluationRead(id = str(evaluation.id), 
        score=str(evaluation.score), details = evaluation.details, creation_date= str(evaluation.creation_date), 
        project_id = str(evaluation.project_id), person_id = str(evaluation.person_id),
             member_id= str(evaluation.member_id)) for evaluation in evaluations]

    """def delete_technology(self, technology_id: int)-> Optional[int]:
        technology = self.db.query(models.Technology).filter(models.Technology.id == technology_id).delete()
        self.db.commit()
        return technology"""
 
  