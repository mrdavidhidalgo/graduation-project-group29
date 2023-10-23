from typing import Optional
from services.commons import base
from services.user.contracts import user_repository
from services.user.model import user_model

class FakeUserRepository(user_repository.UserRepository):
    
    def __init__(self, password : str = "12", username: Optional[str]= None, ) -> None:
        super().__init__()
        self.username = username
        self.password = password
    
    def get_by_username(self, username: str)-> Optional[user_model.User]:
        return None if self.username is None else user_model.User(username=username, 
                                                             password=self.password, 
                                                             is_active=True,
                                                             role = user_model.UserRole.CLIENT,person_id="123")
        
    def save(self, user: user_model.User)-> None:
        ...