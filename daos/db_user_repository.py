from typing import Optional
from .db_model import db_model as models

from services.user.contracts import user_repository

from sqlalchemy.orm import Session

from services.user.model import user_model

class DBUserRepository(user_repository.UserRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_username(self, username: str)-> Optional[user_model.User]:
        user = self.db.query(models.User).filter(models.User.username == username).first()
        #return user_model.User(username="frank", password = "remb", name = "Franklin", is_active=True)
        return None if user is None else user_model.User(username=username, password = user.password, name = user.name, is_active=user.active)
        
    def save(self, user: user_model.User)-> None:
        new_user = models.User(
            username = user.username,
            name = user.name,
            password = user.password,
            active = user.is_active
        )
        
        self.db.add(new_user)
        self.db.commit()