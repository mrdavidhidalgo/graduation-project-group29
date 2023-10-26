from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, Enum, ForeignKey, Text, func
import datetime
from services.commons import base

from .database import Base
from sqlalchemy.orm import relationship
from services.user.model import user_model


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