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
        return None if person is None else person_model.Person(document=document, documentType=person.documentType, firstName = person.firstName, lastName = person.lastName, phoneNumber= person.phoneNumber )
        
    def save(self, person: person_model.Person)-> None:
        new_person = models.Person(
            document = person.document,
            documentType = person.documentType,
            firstName = person.firstName,
            lastName = person.lastName,
            phoneNumber = person.phoneNumber
        )
        
        self.db.add(new_person)
        self.db.commit()

    def get_all_professionals(self)-> Optional[List[person_model.Person]]:
        
        professional = self.db.query(models.Person).all()
        if len(professional) ==0:
            LOGGER.info("There are not prof records")
            return None
        else:
            LOGGER.info("Sendind prof list")
            return [person_model.Person(document=person.document, documentType=person.documentType,
             firstName = person.firstName, lastName = person.lastName, phoneNumber= person.phoneNumber ) 
            for person in professional]