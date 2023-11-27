from typing import Optional, List
from .db_model import db_model as models
from sqlalchemy import text, select
from services.project.contracts import member_repository

from sqlalchemy.orm import Session

from services.project.model import member_model
from services import logs
LOGGER = logs.get_logger()

class DBMemberRepository(member_repository.MemberRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
    
    def get_by_member_id(self, person_id: str, project_id: str)->Optional[member_model.MemberRead]:
        #members = self.db.query(models.ProjectMember).filter(models.ProjectMember.person_id == person_id, models.ProjectMember.project_id == project_id).all()
        members = self.db.execute(text("SELECT * from project_member where person_id='" + str(person_id) + "' and project_id='"+ project_id + "'" ))
        #print("SELECT * from project_member where person_id='" + str(person_id) + "' and project_id='"+ project_id + "'")
        LOGGER.info("SELECT * from project_member where person_id='" + str(person_id) + "' and project_id='"+ project_id + "'")
        LOGGER.info("Filter in repository: [%s]-[%s]", person_id, project_id)
        count = len(members.all())
        LOGGER.info(str(count))
        return None if count==0 else [member_model.MemberRead(id = member.id, active=member.active,\
            description = member.description, person_id = member.person_id, profile_id = member.profile_id,\
            project_id = member.project_id) for member in members]
    
    """def get_all(self)->Optional[List[member_model.MemberRead]]:
        
        members = self.db.query(models.ProjectMember).all()
        if len(members) ==0:
            LOGGER.info("There are not members records")
            None
        else:
            LOGGER.info("Sending members list")
            return [member_model.MemberRead(id = member.id, active=member.active,\
            description = member.description, professional_id = member.professional_id, profile_id = member.profile_id,\
            project_id = member.project_id) for member in members]"""
                
    def save(self, member: member_model.MemberCreate)-> None:
        new_member = models.ProjectMember(
            active = member.active,
            description = member.description,
            person_id = member.person_id,
            profile_id = member.profile_id,
            project_id = member.project_id
            )
        self.db.add(new_member)
        self.db.commit()
        
    def get_by_project_id(self, project_id: str)->Optional[List[member_model.MemberRead]]:
        members = self.db.query(models.ProjectMember).filter(models.ProjectMember.project_id == project_id).all()
        LOGGER.info("Filter in repository: [%s]-[%s]", project_id, str(members))
        
        return None if members is None else [member_model.MemberRead(id = member.id, active=member.active,\
            description = member.description, person_id = member.person_id, profile_id = member.profile_id,\
            project_id = member.project_id) for member in members]
    

    def get_all(self)->List[member_model.MemberRead]:
        members = self.db.query(models.ProjectMember).all()
        return None if members is None else [member_model.MemberRead(id = member.id, active=member.active,\
            description = member.description, person_id = member.person_id, profile_id = member.profile_id,\
            project_id = member.project_id) for member in members]
    
        
    """def delete_technology(self, technology_id: int)-> Optional[int]:
        technology = self.db.query(models.Technology).filter(models.Technology.id == technology_id).delete()
        self.db.commit()
        return technology"""
 
  