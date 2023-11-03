from typing import Optional, List
from datetime import datetime, timedelta
from services.commons import base
from services.professional.contracts import professional_repository
from services.professional.model import professional_model
#from factory.alchemy import SQLAlchemyModelFactory
from unittest.mock import MagicMock, patch
session = MagicMock()

class FakeProfesionalRepository(professional_repository.ProfessionalRepository):
    
    def __init__(self, person_id: Optional[str]= None) -> None:
        super().__init__()
        self.person_id = person_id
    
    def get_by_person_id(self, person_id: str)-> Optional[professional_model.ProfessionalReadModel]:
        return None if self.person_id is None else professional_model.ProfessionalReadModel(id=1, 
                                                                                            birth_date="2023-05-01",
                                                                                            age=35, 
                                                                                            origin_country=base.Country.Colombia,
                                                                                            residence_country=base.Country.Colombia,
                                                                                            residence_city="Santa Marta",
                                                                                            address="Calle 125", 
                                                                                            person_id=person_id)
        
    def save(self, professional: professional_model.ProfessionalCreateModel)-> None:
        ...
        
    def add_academic_info(self, professional_id : int, academic_info: professional_model.ProfessionalAcademicInfo)-> None:
        ...
        
    def add_laboral_info(self, professional_id : int, laboral_info: professional_model.ProfessionalLaboralInfo)-> None:
        ...
        
    def add_technology_info(self, professional_id : int, technology_info: professional_model.ProfessionalTechnologyInfo)-> None:
        ...
        
    def add_technical_role_info(self, professional_id : int, technical_role_info: professional_model.ProfessionalTechnicalRole)-> None:
        ...
        
    """def delete_professional(self, person_id: int)-> Optional[int]:
        return 1"""

    def search_for_candidates(self, role_filter: str, role: str, role_experience: str,technologies_list: list,\
    abilities_list: list, title_filter: str, title: str, title_experience: str)->Optional[List[professional_model.ProfessionalSearchResult]]:
    
        #LOGGER.info("Profesional search")
    
        
        result_candidate_list = []
        
        if len(technologies_list) > 0:
            filter_technology= self.build_filter(technologies_list, "pt.name")
        #LOGGER.info("Filtro de Tecnologia : [%s] y long [%d]",filter_technology, len(technologies_list))
        """"if len(abilities_list) > 0:
            filter_technology=" and pt.name in (" + tech_list + ")"""""
        filter_role=""
        if len(role) > 0:
            if role_filter == "contains":
                filter_role= " and ptr.role like '%" + role + "%'"
            elif role_filter == "starts":
                filter_role= " and ptr.role like '" + role + "%'"
            else:
                filter_role= " and ptr.role = '" + role + "'"

            filter_role=filter_role + " and ptr.experience_years >= '" + str(role_experience) + "'"
        #LOGGER.info("Filtro de Roles de : [%s]",filter_role)
    
        filter_title=""
        if len(title) > 0:
            if title_filter == "contains":
                filter_title= " and pa.title like '%" + title + "%'"
            elif title_filter == "starts":
                filter_title= " and pa.title like '" + title + "%'"
            else:
                filter_title= " and pa.title = '" + title + "'"

            filter_title= filter_title + " and FLOOR(DATEDIFF(now(), pa.end_date)/365) >= '" + str(title_experience) + "'"

        #LOGGER.info("Filtro de Titulos de : [%s]",filter_title)
        
        
        
        return None if (len(role)==0) & (len(title)==0) & (len(technologies_list)==0)\
            else [professional_model.ProfessionalSearchResult(person_id = "1",
                first_name= "Andres",
                last_name="Gomez", 
                age = "30",
                roles = [{'roles': 'PROGRAMADOR[5]'}],
                titles = [{'title': 'ING SISTEMAS[8]'}],
                technologies= [{'name': 'JAVA[5]'}],
                abilities= [{'name': 'Ninguna'}],
                score= "9"
        )]
        
    def date_compare(self, date1, date2)->int:
        date_aux1=datetime.strptime(date1, '%Y-%m-%d %H:%M')
        date_aux2=datetime.strptime(date2, '%Y-%m-%d %H:%M')
        years_diff = (date_aux1 - date_aux2) / timedelta(days=365)
        return int(years_diff)

    def build_filter(self, array_list: list, column:str)->str:
        new_list=""
        filter=""
        for j in array_list:
            if len(str(j)) > 0:
                new_list=new_list + "'" + str(j) + "',"
        new_list=new_list[0:-1]
        if len(new_list) > 0:
            filter=" and " + column + " in (" + new_list + ")"
        return filter