

from datetime import timedelta
import datetime
from typing import List, Optional

from services.technology.contracts import technology_repository
from services.technology import technology_service
from services.technology.model import technology_model
from pydantic import BaseModel
from services.commons import base

import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class TechnologyAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Technology  exists"
        super().__init__(self.message)
        
class CreateTechnologyRequest(BaseModel):
    technology_name : str
    details : str
    category : base.TechnologyCategory

def create_technology(request : CreateTechnologyRequest, technology_repository: technology_repository.TechnologyRepository)-> None:
    
    LOGGER.info("Creating Technology with Name [%s]", request.technology_name)
    
    persisted_technology = technology_repository.get_by_name(technology_name = request.technology_name)
    
    if persisted_technology is not None:
        raise TechnologyAlreadyExistError()
        
    technology_repository.save(
        technology=technology_model.TechnologyCreate(
            technology_name = request.technology_name,
            details = request.details,
            category = request.category
            )
        )


def get_by_name(technology_repository: technology_repository.TechnologyRepository, technology_name: str)-> Optional[technology_model.TechnologyRead]:
    LOGGER.info("Search for ptechnology by name")
    technology = technology_repository.get_by_name(technology_name = technology_name)
    if technology is None:
        LOGGER.info("Technology not exists")
        return None
    else:
        LOGGER.info("Technology exists in service")
        return technology
        
def get_all(technology_repository: technology_repository.TechnologyRepository)->Optional[List[technology_model.TechnologyRead]]:
    LOGGER.info("Search for technologies in service")
    list = technology_repository.get_all()
    if list is None:
        LOGGER.info("Empty List technology in service")
        return None
    else:
        LOGGER.info("Technlogy List with data in service")
        return list
