from datetime import datetime, timedelta
from typing import Annotated, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text 
from daos.db_model.database import SessionLocal, Base
from services.commons import base
from daos.db_model import db_model as models
from controllers import management_service_facade, commons
from services import logs
LOGGER = logs.get_logger()
from daos.db_model.db_model import ProfessionalAcademicInfo as PAI
from daos.db_model.db_model import ProfessionalTechnicalRoleInfo as PTRI
from daos.db_model.db_model import ProfessionalTechnologyInfo as PTI
from daos.db_model.db_model import Professional as PR
from daos.db_model.db_model import Person as PE

session = SessionLocal()
db = Session()


def initialize_technologies():
    #LOGGER.info("Peticion [%s] - [%s]", str(request.document), str(request.documentType))
    
        technologies= session.query(models.Technology).count()
        #session.query(models.Technology).
        LOGGER.info("Technologies number [%s]", str(technologies))
        if int(technologies) < 1:
            t1 = models.Technology(technology_name = "Python",
                details = "Language Python", category = "Develop")

            

            t2 = models.Technology(technology_name = "Java",
                details = "Java Environment", category = "Develop")
            

            t3 = models.Technology(technology_name = "Javascript",
                details = "JavaScript Web Language", category = "Develop")
            

            t4 = models.Technology(technology_name = "C++",
                details = "C++ language", category = "Develop")
            

            t5 = models.Technology(technology_name = "DevOps",
                details = "Practices and Deploy", category = "Virtualization")
            

            t6 = models.Technology(technology_name = "Ruby",
                details = "RUBY on Rails Language", category = "Develop")
            

            t7 = models.Technology(technology_name = "Cypress",
                details = "Testing Technology", category = "Testing")
            session.add_all([t1,t2,t3,t4,t5,t6,t7])
        
            session.commit()
  
def initialize_abilities():
    #LOGGER.info("Peticion [%s] - [%s]", str(request.document), str(request.documentType))
    
        abilities= session.query(models.Ability).count()
        #session.query(models.Technology).
        LOGGER.info("Abilities number [%s]", str(abilities))
        if int(abilities) < 1:
            h1 = models.Ability(ability_name = "Adaptacion",
                details = "Es la habilidad de los trabajadores para afrontar cambios y adecuarse al entorno", category = "SOFT")
            
            h2 = models.Ability(ability_name = "Toma Decisiones",
                details = "saber actuar de manera ágil y rápida ante los posibles problemas que se puedan presentar", category = "SOFT")
            
            h3 = models.Ability(ability_name = "Resiliencia",
                details = "capacidad de superar los obstáculos que afecten su productividad y aprender del fracaso", category = "SOFT")
                
            h4 = models.Ability(ability_name = "Creatividad",
                details = "Una persona creativa apuesta por la innovación, genera nuevas ideas y alimenta su curiosidad", category = "SOFT")
            
            h5 = models.Ability(ability_name = "Colaboracion",
                details = "Propende por ayudar en el trabajo de sus compañeros", category = "SOFT")
                
            h6 = models.Ability(ability_name = "Trabajo Equipo",
                details = "Genera valor a partir de la sinergia con el equipo de trabajo que lo acompaña", category = "SOFT")
                
            h7 = models.Ability(ability_name = "Programacion Web",
                details = "Conocimiento y experiencia en manejo de herramientas Web", category = "HARD")
                
            h8 = models.Ability(ability_name = "Programacion movil",
                details = "Conocimiento y experiencia en manejo de apps para moviles", category = "HARD")
            
            h9 = models.Ability(ability_name = "Proyectos",
                details = "Conocimiento y experiencia en administracion de proyectos", category = "HARD")    
                
            h10 =    models.Ability(ability_name = "Pensamiento Flexible",
                details = "Habilidad para adptarse a cambios de negocio y elaboracion de nuevas estrategias", category = "COGNITIVE") 
            
            session.add_all([h1,h2,h3,h4,h5,h6,h7,h8,h9,h10])
        
            session.commit()

