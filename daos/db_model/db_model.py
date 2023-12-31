from typing import Optional
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, Enum, ForeignKey, Text, func,Date
import datetime
from services.commons import base

from .database import Base
from sqlalchemy.orm import relationship
from services.user.model import user_model
from sqlalchemy import UniqueConstraint

class Person(Base):
    __tablename__ = "person"
    
    document = Column(String(30), primary_key=True, index=True)
    document_type = Column(Enum(base.DocumentType))
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone_number = Column(String(20))
    #users = relationship('User', cascade='all, delete, delete-orphan')
    #professional = relationship('Professional', uselist=False, back_populates="person")

class Professional(Base):
    __tablename__ = "professional"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    birth_date = Column(String(10))
    age = Column(Integer)
    origin_country = Column(Enum(base.Country))
    residence_country = Column(Enum(base.Country))
    residence_city = Column(String(70))
    address = Column(String(100))
    person_id = Column(String(30), ForeignKey('person.document'))
    #person = relationship("Person", back_populates="professional")
    
class User(Base):
    __tablename__ = "user"
    
    username = Column(String(60), primary_key=True, index=True)
    password = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(String(2), primary_key=True, index=True)
    role = Column(Enum(user_model.UserRole))
    person_id = Column(String(30), ForeignKey('person.document'))
    
class ProfessionalAcademicInfo(Base):
    __tablename__ = "professional_academic_info"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    professional_id = Column(Integer, ForeignKey('professional.id'))
    title = Column(String(20))
    institution = Column(String(20))
    country = Column(Enum(base.Country))
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    description = Column(String(20))
    
class ProfessionalLaboralInfo(Base):
    __tablename__ = "professional_laboral_info"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    professional_id = Column(Integer, ForeignKey('professional.id'))
    position = Column(String(50), comment="position or work performed by the professional in the company")
    company_name = Column(String(50))
    company_country = Column(Enum(base.Country))
    company_address = Column(String(100))
    company_phone = Column(String(20), comment="Company contact phone number")
    start_date = Column(DateTime, comment="Start date of the position")
    end_date = Column(DateTime, nullable=True, comment="End date of the position")
    description = Column(String(500), comment= "description of the employee's functions in the company")
    
class ProfessionalTechnicalRoleInfo(Base):
    __tablename__ = "professional_technical_role_info"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    professional_id = Column(Integer, ForeignKey('professional.id'))
    role = Column(String(50), comment="Technical role performed")
    experience_years = Column(Integer)
    description = Column(String(500), comment= "Description of the functions of the role")
    
class ProfessionalTechnologyInfo(Base):
    __tablename__ = "professional_technology_info"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    professional_id = Column(Integer, ForeignKey('professional.id'))
    name = Column(String(50))
    level = Column(Integer)
    experience_years = Column(Integer)
    description = Column(String(500))
    
class Company(Base):
    __tablename__ = "company"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    taxpayer_id = Column(String(20))
    name = Column(String(100))
    country = Column(Enum(base.Country))
    city = Column(String(70))
    years = Column(Integer)
    address = Column(String(100))
    phone_number = Column(String(20))
    #employees = relationship('Employee', cascade='all, delete, delete-orphan')
    
class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile = Column(String(50))
    position = Column(String(100))
    person_id = Column(String(30))
    company_id = Column(String(30))


class Project(Base):
    __tablename__ = "project"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_name = Column(String(100))
    start_date = Column(Date)
    active = Column(Boolean, default=True)
    creation_time = Column(DateTime(timezone=False), server_default=func.now())
    details = Column(Text)
    company_id = Column(String(30))
 

class Test(Base):
    __tablename__ = "test"
    
    name = Column(String(200), primary_key=True, index=True)
    technology = Column(String(200))
    duration_minutes = Column(Integer)
    start_date = Column(Date, default=datetime.datetime.utcnow)
    end_date = Column(Date, default=datetime.datetime.utcnow)
    status =  Column(Enum(base.TestStatus))
    description = Column(String(5000))

class TestResult(Base):
    __tablename__ = "test_result"
    
    test_name = Column(String(200), primary_key=True, index=True)
    candidate_document = Column(String(200), primary_key=True, index=True)
    observation = Column(String(200),nullable=True)
    points = Column(Integer)


class Technology(Base):
    __tablename__ = "technology"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    technology_name = Column(String(100))
    details = Column(Text)
    category = Column(Enum(base.TechnologyCategory))
    



    

class Profile(Base):
    __tablename__ = "profile"
    
    name = Column(String(200), primary_key=True, index=True)
    description = Column(String(500))
    role = Column(String(200))
    experience_in_years =  Column(Integer)
    technology = Column(String(200))
    category = Column(String(200))
    title = Column(String(200))
    project_id = Column(String(200))
    
    
class ProjectMember(Base):
    __tablename__ = "project_member"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    active = Column(Boolean, default=True)
    description = Column(Text)
    person_id = Column(String(30))
    profile_id = Column(String(200))
    project_id = Column(String(20))
    
    
class Ability(Base):
    __tablename__ = "ability"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ability_name = Column(String(100))
    details = Column(Text)
    category = Column(Enum(base.AbilityCategory))
    
class CandidateAbility(Base):
    __tablename__ = "interviews_result_ability"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey('interviews_result.id'))
    ability_id = Column(Integer, ForeignKey('ability.id'))
    qualification= Column(Integer)
    
class CandidateInterview(Base):
    __tablename__ = "interviews_result"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    candidate_document = Column(String(200), index=True)
    project_id = Column(String(60), index=True)
    profile_id = Column(String(200), index=True)
    date = Column(Date, default=datetime.datetime.utcnow)
    recording_file = Column(String(60), nullable=True)
    test_file = Column(String(60), nullable=True)
    observation = Column(String(500))

    __table_args__ = (UniqueConstraint("candidate_document", "project_id","profile_id"), )


class PerformaceEvaluation(Base):
    __tablename__ = "performance_evaluation"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    score = Column(Integer)
    details = Column(Text)
    creation_date = Column(Date, default=datetime.datetime.utcnow)
    project_id = Column(String(20))
    person_id = Column(Integer)
    member_id = Column(Integer)


class Interview(Base):
    __tablename__ = "interviews"
    candidate_document = Column(String(200), primary_key=True, index=True)
    project_id = Column(String(200), primary_key=True, index=True)
    profile_id= Column(String(200), primary_key=True, index=True)
    status = Column(String(200))
    meet_url =  Column(String(200))
    start_timestamp =Column(DateTime)  
    duration_minutes= Column(Integer)  
    
