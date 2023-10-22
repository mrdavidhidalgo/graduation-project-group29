import abc
from services.company.model import company_model
from typing import List

class CompanyRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_taxpayerId(self, taxpayerId: str)-> company_model.Company:
        ...
        
    @abc.abstractmethod
    def save(self, company: company_model.Company)-> None:
        ...
        
    @abc.abstractmethod
    def get_all(self)->List[company_model.Company]:
        ...