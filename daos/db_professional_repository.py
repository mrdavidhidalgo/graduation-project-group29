from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import text, select
from .db_model import db_model as models
from sqlalchemy.exc import SQLAlchemyError

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
        
    def get_full_info(self, professional_id: int)-> List[professional_model.ProfessionalFullInfo]:
        
        professional_db = self.db.query(models.Professional).filter(models.Professional.person_id == professional_id).first()
       
        professional = professional_model.ProfessionalReadModel(id = professional_db.id, 
                                                                birth_date = professional_db.birth_date , 
                                                                age=professional_db.age,
                                                                origin_country= professional_db.origin_country,
                                                                residence_country = professional_db.residence_country, 
                                                                residence_city = professional_db.residence_city,
                                                                address = professional_db.address, 
                                                                person_id = professional_id )
        
        LOGGER.info("Finding academic info for %s", professional_id)
        academics = self.db.query(models.ProfessionalAcademicInfo).filter(models.ProfessionalAcademicInfo.professional_id == professional.id)
        
        academic_info = [professional_model.ProfessionalAcademicInfo(person_id=professional_id, 
                                                        title=academic_info.title, 
                                                        institution=academic_info.title, 
                                                        country = academic_info.country,
                                                        start_date=academic_info.start_date,
                                                        end_date=academic_info.end_date,
                                                        description=academic_info.description) for academic_info in academics]
        
        LOGGER.info("Finding laboral info for %s", professional_id)
        laborals = self.db.query(models.ProfessionalLaboralInfo).filter(models.ProfessionalLaboralInfo.professional_id == professional.id)
        laboral_info = [professional_model.ProfessionalLaboralInfo(person_id = professional_id,
                                                                    position = laboral_info.position,
                                                                    company_name= laboral_info.company_name,
                                                                    company_country = laboral_info.company_country,
                                                                    company_address =  laboral_info.company_address,
                                                                    company_phone = laboral_info.company_phone,
                                                                    start_date = laboral_info.start_date,
                                                                    end_date = laboral_info.end_date,
                                                                    description = laboral_info.description) for laboral_info in laborals]
        
        LOGGER.info("Finding technology info for %s", professional_id)
        tecnologies = self.db.query(models.ProfessionalTechnologyInfo).filter(models.ProfessionalTechnologyInfo.professional_id == professional.id)
        technology_info = [professional_model.ProfessionalTechnologyInfo(person_id = professional_id,
                                                                         name = technology_info.name,
                                                                         experience_years = technology_info.experience_years,
                                                                         level = technology_info.level,
                                                                         description = technology_info.description) for technology_info in tecnologies]
        
        return professional_model.ProfessionalFullInfo(basic_info=professional, 
                                                       laboral_info=laboral_info,
                                                       academic_info=academic_info,
                                                       technology_info=technology_info)
        
    
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

            test = self.db.execute(text("SELECT t.technology,r.points from test as t, test_result as r where t.name=r.test_name\
                and r.candidate_document='" + str(p.document) + "' order by t.technology"))

            #LOGGER.info("Profesional: [%d] - [%s] - [%s] - [%d]",p.id, p.first_name,p.last_name, p.age)

            roles=""
            for r in rol:
                LOGGER.info("Roles de : [%s] - [%s] - Experiencia [%d] ",p.first_name,r.role, r.experience_years)
                roles=roles + r.role + "[" + str(r.experience_years) + "],"
            roles=roles[0:-1]

            if (len(roles)==0) & (len(filter_role) > 1):
                continue

            titles=""
            for ac in academic:
                years = self.date_compare(datetime.now().strftime("%Y-%m-%d %H:%M"), ac.end_date.strftime("%Y-%m-%d %H:%M"))
                LOGGER.info("Titulos de : [%s] - [%s] - Experiencia [%d] ",p.first_name,ac.title, years)
                titles=titles + ac.title + "[" + str(years) + "],"
            titles=titles[0:-1]    
                
            abilities="Ninguna"
           
            
            if (len(titles)==0) & (len(filter_title) > 1):
                continue

            technologies=""
            for ti in technology:
                LOGGER.info("Tecnologias de : [%s] - [%s] - Nivel [%d] ",p.first_name,ti.name, ti.level)
                technologies=technologies + ti.name + "[" + str(ti.level) + "],"
            technologies=technologies[0:-1]      

            if (len(technologies)==0) & (len(filter_technology) > 0):
                continue

            tests=""
            for t in test:
                LOGGER.info("Tests de : [%s] - [%s] - Experiencia [%d] ",p.first_name,t.technology, t.points)
                tests=tests + t.technology + "[" + str(t.points) + "],"
            tests=tests[0:-1]


            new_record = professional_model.ProfessionalSearchResult(
                person_id = p.document,
                first_name= p.first_name,
                last_name= p.last_name, 
                age = p.age,
                roles = roles,
                titles = titles,
                technologies= technologies,
                abilities= abilities,
                score= tests
            )
            result_candidate_list.append(new_record)  
            LOGGER.info("Profesional: [%d] valid",p.id,)
        
        
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
    
    def get_candidates_without_interviews(self)->List[professional_model.ProfessionalReadModel]:
        
        query = select(models.Professional).outerjoin(models.CandidateInterview, models.Professional.id == models.CandidateInterview.profesional_id).filter(models.CandidateInterview.id.is_(None))
        result = self.db.execute(query)
        
        return list(map(lambda row: professional_model.ProfessionalReadModel(id = row.id,
                                                                             birth_date = row.birth_date,
                                                                             age= row.age,
                                                                             origin_country =row.origin_country,
                                                                             residence_country = row.residence_country,
                                                                             residence_city = row.residence_city,
                                                                             address = row.residence_city,
                                                                             person_id = row.person_id), result.scalars().all()))
        
        

        
    
