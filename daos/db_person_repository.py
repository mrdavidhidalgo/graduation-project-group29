from typing import Optional, List
from .db_model import db_model as models

from services.person.contracts import person_repository

from sqlalchemy.orm import Session

from services.person.model import person_model
from services import logs


LOGGER = logs.get_logger()

class DBPersonRepository(person_repository.PersonRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_document(self, document: int)-> Optional[person_model.Person]:
        person = self.db.query(models.Person).filter(models.Person.document == document).first()
        #return user_model.User(username="frank", password = "remb", name = "Franklin", is_active=True)
        return None if person is None else person_model.Person(document=document, 
                                                               document_type=person.documentType, 
                                                               first_name = person.firstName, 
                                                               last_name = person.lastName, 
                                                               phone_number= person.phoneNumber )
        
    def save(self, person: person_model.Person)-> None:
        new_person = models.Person(
            document = person.document,
            documentType = person.document_type,
            firstName = person.first_name,
            lastName = person.last_name,
            phoneNumber = person.phone_number
        )
        
        self.db.add(new_person)
        self.db.commit()

    def get_all(self)-> Optional[List[person_model.Person]]:
        
        professional = self.db.query(models.Person).all()
        if len(professional) ==0:
            LOGGER.info("There are not person records")
            return []
        else:
            LOGGER.info("Sendind person list")
            return [person_model.Person(document=person.document, document_type=person.documentType,
             first_name = person.firstName, last_name = person.lastName, phone_number= person.phoneNumber ) 
            for person in professional]