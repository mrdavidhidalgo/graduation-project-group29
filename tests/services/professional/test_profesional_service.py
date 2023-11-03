import datetime
from services.commons import base
from services.professional import professional_service as subject
from services.professional.model import professional_model
from tests.services.professional import mocks
import pytest


###########################################################################################
#                                   create_professional()                                 #
###########################################################################################

@pytest.mark.unittests
def test_should_raise_exception_trying_to_create_professionl_but_it_already_exist()->None:
    
    with pytest.raises(subject.ProfessionalAlreadyExistError):
        subject.create_professional(
            birth_date ="2023-02-01",
            age = 18,
            origin_country= base.Country.Colombia, 
            residence_country= base.Country.Colombia, 
            residence_city = "Medellin", 
            address = "Calle 15", 
            person_id = "123", 
            professional_repository= mocks.FakeProfesionalRepository(person_id="23")
        )
        
@pytest.mark.unittests
def test_should_create_professional_succesfully()->None:
    
    subject.create_professional(
        birth_date ="2023-02-01",
                        age = 18,
                        origin_country= base.Country.Colombia, 
                        residence_country= base.Country.Colombia, 
                        residence_city = "Medellin", 
                        address = "Calle 15", 
                        person_id = "123", 
                        professional_repository= mocks.FakeProfesionalRepository()
    )
    
###########################################################################################
#                                     add_academic_info()                                 #
###########################################################################################

@pytest.mark.unittests
def test_should_raise_exception_trying_to_add_academic_info_but_professional_does_not_exist()->None:
    
    with pytest.raises(subject.ProfessionalDoesNotExistError):
        subject.add_academic_info(
            academic_info = professional_model.ProfessionalAcademicInfo(
                person_id ="1",
                title ="Ingeniero",
                institution ="Unimag",
                country = base.Country.Colombia,
                start_date = datetime.datetime.now(),
                end_date =datetime.datetime.now(),
                description ="Especialidad"
            ), 
            professional_repository=mocks.FakeProfesionalRepository()
        )
        

@pytest.mark.unittests
def test_should_create_academic_info_succesfully()->None:
    
    subject.add_academic_info(
        academic_info = professional_model.ProfessionalAcademicInfo(
            person_id ="1",
            title ="Ingeniero",
            institution ="Unimag",
            country = base.Country.Colombia,
            start_date = datetime.datetime.now(),
            end_date =datetime.datetime.now(),
            description ="Especialidad"
        ), 
        professional_repository=mocks.FakeProfesionalRepository(person_id="1")
    )
    
###########################################################################################
#                                     add_laboral_info()                                  #
###########################################################################################

@pytest.mark.unittests
def test_should_raise_exception_trying_to_add_laboral_info_but_professional_does_not_exist()->None:
    
    with pytest.raises(subject.ProfessionalDoesNotExistError):
        subject.add_laboral_info(
            laboral_info = professional_model.ProfessionalLaboralInfo(
                person_id ="1",
                position ="Ingeniero Senior",
                company_name = "Proyectos LTDA",
                company_country = base.Country.Colombia,
                company_address = "Calle 98",
                company_phone = "4215256",
                start_date = datetime.datetime.now(),
                end_date = datetime.datetime.now(),
                description = "funciones varias"
            ), 
            professional_repository=mocks.FakeProfesionalRepository()
        )
        

@pytest.mark.unittests
def test_should_create_laboral_info_succesfully()->None:
    
    subject.add_laboral_info(
        laboral_info = professional_model.ProfessionalLaboralInfo(
            person_id ="1",
            position ="Ingeniero Senior",
            company_name = "Proyectos LTDA",
            company_country = base.Country.Colombia,
            company_address = "Calle 98",
            company_phone = "4215256",
            start_date = datetime.datetime.now(),
            end_date = datetime.datetime.now(),
            description = "funciones varias"
        ), 
        professional_repository=mocks.FakeProfesionalRepository(person_id="1")
    )
    
###########################################################################################
#                                   add_technical_role()                                  #
###########################################################################################

@pytest.mark.unittests
def test_should_raise_exception_trying_to_add_technical_role_but_professional_does_not_exist()->None:
    
    with pytest.raises(subject.ProfessionalDoesNotExistError):
        subject.add_technical_role(
            technical_role = professional_model.ProfessionalTechnicalRole(
                person_id ="1",
                role ="Ingeniero de soporte",
                experience_years=5,
                description="Varios"
            ), 
            professional_repository=mocks.FakeProfesionalRepository()
        )
        

@pytest.mark.unittests
def test_should_add_technical_role_succesfully()->None:
    
    subject.add_technical_role(
        technical_role = professional_model.ProfessionalTechnicalRole(
            person_id ="1",
            role ="Ingeniero de soporte",
            experience_years=5,
            description="Varios"
        ), 
        professional_repository=mocks.FakeProfesionalRepository(person_id="1")
    )
    
###########################################################################################
#                                  add_technology_info()                                  #
###########################################################################################

@pytest.mark.unittests
def test_should_raise_exception_trying_to_add_technology_info_but_professional_does_not_exist()->None:
    
    with pytest.raises(subject.ProfessionalDoesNotExistError):
        subject.add_technology_info(
            technology_info = professional_model.ProfessionalTechnologyInfo(
                person_id ="1",
                name = "Java",
                experience_years = 3,
                level = 3,
                description = "Como lenguaje"
            ), 
            professional_repository=mocks.FakeProfesionalRepository()
        )
        

@pytest.mark.unittests
def test_should_add_technology_info_succesfully()->None:
    
    subject.add_technology_info(
        technology_info= professional_model.ProfessionalTechnologyInfo(
            person_id ="1",
            name = "Java",
            experience_years = 3,
            level = 3,
            description = "Como lenguaje"
        ), 
        professional_repository=mocks.FakeProfesionalRepository(person_id="1")
    )

###########################################################################################
#                                  search_for_candidates()                                #
###########################################################################################

@pytest.mark.unittests
def test_should_get_candidates_sucessfully()->None:
    
    subject.search_for_candidates(subject.CandidateSearchRequest(
        role_filter = "contains",
        role = "",
        role_experience = "2",
        technologies = ["JAVA","PYTHON"],
        abilities = [],
        title_filter = "start",
        title = "PR",
        title_experience = "3"),
        professional_repository= mocks.FakeProfesionalRepository()
    )
    
    
def test_should_get_candidates_not_found()->None:
   
    search_result = subject.search_for_candidates(subject.CandidateSearchRequest(
        role_filter = "contains",
        role = "",
        role_experience = "15",
        technologies = [],
        abilities = [],
        title_filter = "start",
        title = "",
        title_experience = "3"),
        professional_repository= mocks.FakeProfesionalRepository()
    )
    assert search_result is None