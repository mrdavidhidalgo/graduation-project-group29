from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum, ForeignKey
import datetime
from services.commons import base

from .database import Base
from sqlalchemy.orm import relationship
from services.user.model import user_model


class Person(Base):
    __tablename__ = "person"
    
    document = Column(String(30), primary_key=True, index=True)
    documentType = Column(Enum(base.DocumentType))
    firstName = Column(String(50))
    lastName = Column(String(50))
    phoneNumber = Column(String(20))
    #users = relationship('User', cascade='all, delete, delete-orphan')
    #professional = relationship('Professional', uselist=False, back_populates="person")

class Professional(Base):
    __tablename__ = "professional"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    birthDate = Column(String(10))
    age = Column(Integer)
    originCountry = Column(Enum(base.Country))
    residenceCountry = Column(Enum(base.Country))
    residenceCity = Column(String(70))
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
    


class Company(Base):
    __tablename__ = "company"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    taxpayer_Id = Column(String(20))
    name = Column(String(100))
    country = Column(Enum(base.Country))
    city = Column(String(70))
    years = Column(Integer)
    address = Column(String(100))
    phoneNumber = Column(String(20))
    employees = relationship('Employee', cascade='all, delete, delete-orphan')
    
class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile = Column(String(50))
    position = Column(String(100))
    person_id = Column(String(30), ForeignKey('person.document'))
    company_id = Column(String(30), ForeignKey('company.id'))