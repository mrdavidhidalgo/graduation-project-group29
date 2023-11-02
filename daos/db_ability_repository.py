from typing import Optional, List
from .db_model import db_model as models

from services.ability.contracts import ability_repository

from sqlalchemy.orm import Session

from services.ability.model import ability_model
from services import logs
LOGGER = logs.get_logger()

class DBAbilityRepository(ability_repository.AbilityRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
    
    def get_all(self)->List[ability_model.AbilityRead]:
        
        abilities = self.db.query(models.Ability).all()
        if len(abilities) ==0:
            LOGGER.info("There are not abilities records")
            None
        else:
            LOGGER.info("Sending abilities list")
            return [ability_model.AbilityRead(id = ability.id, ability_name=ability.ability_name,\
            details = ability.details, category = ability.category)   for ability in abilities]
                
    def save(self, ability: ability_model.AbilityCreate)-> None:
        new_ability = models.Ability(
            ability_name = ability.ability_name,
            details = ability.details,
            category = ability.category
        )
        
        self.db.add(new_ability)
        self.db.commit()
        

    def get_by_name(self, ability_name: str)->ability_model.AbilityRead:  
        ability = self.db.query(models.Ability).filter(models.Ability.ability_name == ability_name).first()
       
        return None if ability is None else ability_model.AbilityRead(id = ability.id, ability_name=ability.ability_name,\
            details = ability.details, category = ability.category)

    def delete_hability(self, ability_id: int)->Optional[int]:
        ability = self.db.query(models.Ability).filter(models.Ability.id == ability_id).delete()
        self.db.commit()
        return ability
 
  