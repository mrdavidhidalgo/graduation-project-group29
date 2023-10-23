import datetime
from services.commons import base
from services.user import user_service as subject
from services.user.model import user_model
from tests.services.user import mocks
import pytest

###########################################################################################
#                                         create_user()                                   #
###########################################################################################

@pytest.mark.unittests
def test_should_raise_exception_trying_to_create_user_but_username_already_exist()->None:
    
    with pytest.raises(subject.UserNameAlreadyExistError):
        subject.create_user(
            username="ftesst", 
            password = "1234", 
            role = "COMPANY", 
            person_id = "1", 
            user_repository = mocks.FakeUserRepository(username="1")
        )
        
@pytest.mark.unittests
def test_should_create_company_as_user_succesfully()->None:
    
    subject.create_user(
        username="ftesst", 
        password = "1234", 
        role = "COMPANY", 
        person_id = "1", 
        user_repository = mocks.FakeUserRepository()
    )
    
@pytest.mark.unittests
def test_should_create_recruiter_as_user_succesfully()->None:
    
    subject.create_user(
        username="ftesst", 
        password = "1234", 
        role = "RECRUITER", 
        person_id = "1", 
        user_repository = mocks.FakeUserRepository()
    )
    
@pytest.mark.unittests
def test_should_create_candidate_as_user_succesfully()->None:
    
    subject.create_user(
        username="ftesst", 
        password = "1234", 
        role = "CANDIDATE", 
        person_id = "1", 
        user_repository = mocks.FakeUserRepository()
    )
    
###########################################################################################
#                                        login_user()                                     #
###########################################################################################

@pytest.mark.unittests
def test_should_raise_exception_trying_to_login_user_but_user_does_not_exist()->None:
    
    with pytest.raises(subject.UserLoginValidationError):
        subject.login_user(
            username="ftesst", 
            password = "1234", 
            user_repository = mocks.FakeUserRepository()
        )
        
@pytest.mark.unittests
def test_should_raise_exception_trying_to_login_user_but_password_is_invalid()->None:
    
    with pytest.raises(subject.UserLoginValidationError):
        subject.login_user(
            username="ftesst", 
            password = "1234", 
            user_repository = mocks.FakeUserRepository(password="456", username="ftesst")
        )
        
@pytest.mark.unittests
def test_should_login_user_succesfully()->None:
    
    subject.login_user(
        username="ftesst", 
        password = "1234", 
        user_repository = mocks.FakeUserRepository(password="1234", username="ftest")
    )