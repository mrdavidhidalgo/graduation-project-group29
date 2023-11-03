

from datetime import timedelta
import datetime
from typing import List, Optional

from services.ability.contracts import ability_repository
from services.ability import ability_service
from services.ability.model import ability_model
from pydantic import BaseModel
from services.commons import base

import os
import random

from services import logs


LOGGER = logs.get_logger()

                
class AbilityAlreadyExistError(Exception):
     def __init__(self, *args: object) -> None:
        self.message = "Ability  exists"
        super().__init__(self.message)
        
class CreateAbilityRequest(BaseModel):
    ability_name : str
    details : str
    category : base.AbilityCategory

def create_ability(request : CreateAbilityRequest, ability_repository: ability_repository.AbilityRepository)-> None:
    
    LOGGER.info("Creating ability with Name [%s]", request.ability_name)
    
    persisted_ability = ability_repository.get_by_name(ability_name = request.ability_name)
    
    if persisted_ability is not None:
        raise AbilityAlreadyExistError()
        
    ability_repository.save(
        technology=ability_model.AbilityCreate(
            ability_name = request.ability_name,
            details = request.details,
            category = request.category
            )
        )


def get_by_name(ability_repository: ability_repository.AbilityRepository, ability_name: str)-> Optional[ability_model.AbilityRead]:
    LOGGER.info("Search for ability by name")
    ability = ability_repository.get_by_name(ability_name = ability_name)
    if ability is None:
        LOGGER.info("Ability not exists")
        return None
    else:
        LOGGER.info("Ability exists in service")
        return ability
        
def get_all(ability_repository: ability_repository.AbilityRepository)->Optional[List[ability_model.AbilityRead]]:
    LOGGER.info("Search for technologies in service")
    list = ability_repository.get_all()
    if list is None:
        LOGGER.info("Empty List ability in service")
        return None
    else:
        LOGGER.info("Ability List with data in service")
        return list
