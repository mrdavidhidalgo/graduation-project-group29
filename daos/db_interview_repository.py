from typing import Optional
from .db_model import db_model as models
from sqlalchemy.exc import SQLAlchemyError
from services.interview.contracts import interview_model
from typing import List
from sqlalchemy.orm import Session

from services.interview.contracts import interview_repository

class DBInterviewRepository(interview_repository.InterviewRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
    def get_by_project_and_candidate(self, project_id: str,candidate_document: str,profile_id:str)-> Optional[interview_model.Interview]:
        ... 
        interv = self.db.query(models.Interview).filter(models.Interview.candidate_document == candidate_document).filter(models.Interview.project_id == project_id ).filter(models.Interview.profile_id == profile_id ).first() 
        
        return None if interv is None else interview_model.Interview(    
                                                         candidate_document = interv.candidate_document,
                                                         project_id = interv.project_id,
                                                         status = interv.status,
                                                         meet_url = interv.meet_url,
                                                         start_timestamp = interv.start_timestamp,
                                                         profile_id=profile_id,
                                                         duration_minutes = interv.duration_minutes)
        
    def save(self, interview: interview_model.Interview)-> None:
        new_interview = models.Interview(**interview.dict())
        
        self.db.add(new_interview)
        self.db.commit()


    def get_interviews(self,candidate_document: str|None)-> List[interview_model.Interview]:

        interv_query = self.db.query(models.Interview)

        if candidate_document:
            interv_query = interv_query.filter(models.Interview.candidate_document == candidate_document)
        
        interviews=interv_query.order_by(models.Interview.start_timestamp.desc()).all()
        
        return [] if interviews is None else [interview_model.Interview(    
                                                         candidate_document = interv.candidate_document,
                                                         project_id = interv.project_id,
                                                         status = interv.status,
                                                         meet_url = interv.meet_url,
                                                         start_timestamp = interv.start_timestamp,
                                                         profile_id=interv.profile_id,
                                                         duration_minutes = interv.duration_minutes) for interv in interviews]
        
    def load_interview(self, interview_info: interview_model.LoadInterviewInfo)->None:
        

        candidate_interview_info = models.CandidateInterview(
            candidate_document = interview_info.candidate_document,
            project_id = interview_info.project_id,
            profile_id = interview_info.profile_id,
            date = interview_info.date,
            recording_file = interview_info.recording_file,
            test_file = interview_info.test_file,
            observation = interview_info.observation
        )
        
        try:
            with self.db.begin():
                self.db.add(candidate_interview_info)
                self.db.flush()
                interv = self.db.query(models.Interview).filter(models.Interview.candidate_document == interview_info.candidate_document).filter(models.Interview.project_id == interview_info.project_id ).filter(models.Interview.profile_id == interview_info.profile_id ).first() 
                if interv:
                    interv.status="DONE"
                self.db.add(interv)
                abilities = list(map(lambda x: models.CandidateAbility(
                                    interview_id = candidate_interview_info.id,
                                    ability_id = x.ability_id,
                                    qualification= x.qualification), interview_info.abilities))

                self.db.add_all(abilities)
            
        except SQLAlchemyError as e:

            # Si ocurre un error, haz rollback de la transacción
            print(f"Error en la transacción: {e}")
            self.db.rollback()

        finally:
            # Cierra la sesión
            self.db.close() 



    def find_interview_results(self)->List[interview_model.LoadInterviewInfo]:

        interview_results = self.db.query(models.CandidateInterview).all() 

        return [interview_model.LoadInterviewInfo(
                id=interview_info.id,
                candidate_document = interview_info.candidate_document,
                project_id = interview_info.project_id,
                profile_id = interview_info.profile_id,
                date = interview_info.date,
                recording_file = interview_info.recording_file,
                test_file = interview_info.test_file,
                observation = interview_info.observation,
                abilities=[])
                for interview_info in interview_results]       
    

    def find_interview_result(self,  id:int)-> interview_model.LoadInterviewInfo | None:
        interview_info = self.db.query(models.CandidateInterview).filter(models.CandidateInterview.id == id).first() 
        interview_result_ability = self.db.query(models.CandidateAbility).all()

        return interview_model.LoadInterviewInfo(
            id=interview_info.id,
            candidate_document = interview_info.candidate_document,
            project_id = interview_info.project_id,
            profile_id = interview_info.profile_id,
            date = interview_info.date,
            recording_file = interview_info.recording_file,
            test_file = interview_info.test_file,
            observation = interview_info.observation,
            abilities=[interview_model.AbilityInterviewInfo(ability_id=a.ability_id, qualification=a.qualification) for a in interview_result_ability] 
            )
