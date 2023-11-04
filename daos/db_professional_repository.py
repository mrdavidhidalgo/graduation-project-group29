from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import text 
from .db_model import db_model as models

from services import logs
LOGGER = logs.get_logger()

from services.professional.contracts import professional_repository

from sqlalchemy.orm import Session

from services.professional.model import professional_model

class DBProfessionalRepository(professional_repository.ProfessionalRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_person_id(self, person_id: str)-> Optional[professional_model.ProfessionalReadModel]:
        professional = self.db.query(models.Professional).filter(models.Professional.person_id == person_id).first()
       
        return None if professional is None else professional_model.ProfessionalReadModel(id = professional.id, birth_date = professional.birth_date , age=professional.age,\
        origin_country= professional.origin_country, residence_country = professional.residence_country, residence_city = professional.residence_city,\
        address = professional.address, person_id = person_id )
        
    def save(self, professional: professional_model.ProfessionalCreateModel)-> None:
        new_professional = models.Professional(
            birth_date = professional.birth_date,
            age = professional.age,
            origin_country = professional.origin_country,
            residence_country = professional.residence_country,
            residence_city = professional.residence_city,
            address = professional.address,
            person_id = professional.person_id
        )
        
        self.db.add(new_professional)
        self.db.commit()
        
    def add_academic_info(self, professional_id: int, academic_info: professional_model.ProfessionalAcademicInfo)-> None:
        academic_info = models.ProfessionalAcademicInfo(
            professional_id = professional_id,
            title = academic_info.title,
            institution = academic_info.institution,
            country = academic_info.country,
            start_date = academic_info.start_date,
            end_date = academic_info.end_date,
            description = academic_info.description
        )
        
        self.db.add(academic_info)
        self.db.commit()
        
    def add_laboral_info(self, professional_id: int, laboral_info: professional_model.ProfessionalLaboralInfo)-> None:
        laboral_info = models.ProfessionalLaboralInfo(
            professional_id = professional_id,
            position = laboral_info.position,
            company_name = laboral_info.company_name,
            company_country = laboral_info.company_country,
            company_address = laboral_info.company_address,
            company_phone = laboral_info.company_phone,
            start_date = laboral_info.start_date,
            end_date = laboral_info.end_date,
            description = laboral_info.description
        )
        
        self.db.add(laboral_info)
        self.db.commit()
        
    def add_technical_role_info(self, professional_id: int, technical_role_info: professional_model.ProfessionalTechnicalRole)-> None:
        technical_role = models.ProfessionalTechnicalRoleInfo(
            professional_id = professional_id,
            role = technical_role_info.role,
            experience_years = technical_role_info.experience_years,
            description = technical_role_info.description

        )
        
        self.db.add(technical_role)
        self.db.commit()
        
    def add_technology_info(self, professional_id: int, technology_info: professional_model.ProfessionalTechnologyInfo)-> None:
        technology_info = models.ProfessionalTechnologyInfo(
            professional_id = professional_id,
            name = technology_info.name,
            level = technology_info.level,
            experience_years = technology_info.experience_years,
            description = technology_info.description

        )
        
        self.db.add(technology_info)
        self.db.commit()
        
    """def delete_professional(self, person_id: int)-> Optional[int]:
        professional = self.db.query(models.Professional).filter(models.Professional.person_id == person_id).delete()
        self.db.commit()
        return professional 
    """ 
    
    def search_for_candidates(self, role_filter: str, role: str, role_experience: str,technologies_list: list,\
    abilities_list: list, title_filter: str, title: str, title_experience: str)->Optional[List[professional_model.ProfessionalSearchResult]]:
        LOGGER.info("Profesional search")
    
        
        result_candidate_list = []
        
        if len(technologies_list) > 0:
            filter_technology= self.build_filter(technologies_list, "pt.name")
        LOGGER.info("Filtro de Tecnologia : [%s] y long [%d]",filter_technology, len(technologies_list))
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
        LOGGER.info("Filtro de Roles de : [%s]",filter_role)

        filter_title=""
        if len(title) > 0:
            if title_filter == "contains":
                filter_title= " and pa.title like '%" + title + "%'"
            elif title_filter == "starts":
                filter_title= " and pa.title like '" + title + "%'"
            else:
                filter_title= " and pa.title = '" + title + "'"

            filter_title= filter_title + " and FLOOR(DATEDIFF(now(), pa.end_date)/365) >= '" + str(title_experience) + "'"

        LOGGER.info("Filtro de Titulos de : [%s]",filter_title)
        
        professionals = self.db.execute(text("SELECT p.document , p.first_name, p.last_name, pr.age, pr.id  from person as p, professional as pr \
         where pr.person_id = p.document  order by p.first_name" ))
        professionals2= professionals.mappings().all()


        for p in professionals2:
            rol = self.db.execute(text("SELECT ptr.role , ptr.experience_years from professional_technical_role_info as ptr, professional as pr\
             where pr.id = ptr.professional_id and pr.id='" + str(p.id) + "'" + filter_role + " order by ptr.role" ))

            academic = self.db.execute(text("SELECT pa.title , pa.end_date from professional_academic_info as pa, professional as pr\
             where pr.id = pa.professional_id and pr.id='" + str(p.id) + "'" + filter_title + "order by pa.title" ))

            technology = self.db.execute(text("SELECT pt.name, pt.level from professional_technology_info as pt, professional as pr\
             where pr.id = pt.professional_id and pr.id='" + str(p.id) + "'" + filter_technology + " order by pt.name" ))


            LOGGER.info("Profesional: [%d] - [%s] - [%s] - [%d]",p.id, p.first_name,p.last_name, p.age)

            roles=""
            for r in rol:
                LOGGER.info("Roles de : [%s] - [%s] - Experiencia [%d] ",p.first_name,r.role, r.experience_years)
                roles=roles + r.role + "[" + str(r.experience_years) + "],"
            roles=roles[0:-1]
                #roles.append({'role' : aux})

            if (len(roles)==0) & (len(filter_role) > 0):
                continue

            titles=""
            for ac in academic:
                years = self.date_compare(datetime.now().strftime("%Y-%m-%d %H:%M"), ac.end_date.strftime("%Y-%m-%d %H:%M"))
                LOGGER.info("Titulos de : [%s] - [%s] - Experiencia [%d] ",p.first_name,ac.title, years)
                titles=titles + ac.title + "[" + str(years) + "],"
            titles=titles[0:-1]    
                #titles.append({'title' : aux2 })
                    #titles=titles + "," + ac.title

            abilities="Ninguna"
            #abilities.append({'name': 'Ninguna'})
            
            if (len(titles)==0) & (len(filter_title) > 0):
                continue

            technologies=""
            for ti in technology:
                LOGGER.info("Tecnologias de : [%s] - [%s] - Nivel [%d] ",p.first_name,ti.name, ti.level)
                technologies=technologies + ti.name + "[" + str(ti.level) + "],"
            technologies=technologies[0:-1]      
                #technologies.append({'name': aux3})

            if (len(technologies)==0) & (len(technologies_list) > 0):
                continue

            new_record = professional_model.ProfessionalSearchResult(
                person_id = p.document,
                first_name= p.first_name,
                last_name= p.last_name, 
                age = p.age,
                roles = roles,
                titles = titles,
                technologies= technologies,
                abilities= abilities,
                score= ""
            )
            result_candidate_list.append(new_record)  
            LOGGER.info("Profesional: valid")
        
        
        return result_candidate_list

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
