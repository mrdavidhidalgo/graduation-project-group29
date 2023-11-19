import abc
from services.company.model import company_model
from typing import List, Optional

class CompanyRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_by_taxpayerId(self, taxpayer_id: str)-> company_model.Company:
        ...
        
    @abc.abstractmethod
    def save(self, company: company_model.Company)-> None:
        ...
        
    @abc.abstractmethod
    def get_all(self)->List[company_model.Company]:
        ...
        
    @abc.abstractmethod    
    def delete_company(self, taxpayer_id: int)-> Optional[int]:
        ...