import abc
from services.user.model import user_model
from typing import List, Optional

class UserRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_username(self, username: str)-> Optional[user_model.User]:
        ...
        
    @abc.abstractmethod
    def save(self, user: user_model.User)-> None:
        ...
    
    def delete_user(self, username: str)-> Optional[int]:
        ...