import abc
from services.user.model import user_model
from typing import List

class UserRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_username(self, username: str)-> user_model.User:
        ...
        
    @abc.abstractmethod
    def save(self, user: user_model.User)-> None:
        ...
