from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum, ForeignKey
import datetime

from .database import Base
import enum
from sqlalchemy.orm import relationship
from services.user.model import user_model

class Person(Base):
    __tablename__ = "person"
    
    document = Column(String, primary_key=True, index=True)
    documentType = Column(String(30))
    firstName = Column(String(50))
    lastName = Column(String(50))
    phoneNumber = Column(String(20))
    users = relationship('User', cascade='all, delete, delete-orphan')
    professional = relationship('Professional', uselist=False, back_populates="person")

class Professional(Base):
    __tablename__ = "professional"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    birthDate = Column(String(10))
    age = Column(Integer)
    originCountry = Column(String(70))
    residenceCountry = Column(String(70))
    residenceCity = Column(String(70))
    address = Column(String(100))
    person_id = Column(String, ForeignKey('person.document'))
    person = relationship("Person", back_populates="professional")
    
class User(Base):
    __tablename__ = "user"
    
    username = Column(String(60), primary_key=True, index=True)
    password = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(String(2), primary_key=True, index=True)
    role = Column(Enum(user_model.UserRole))
    person_id = Column(String, ForeignKey('person.document'))
    
class ProfessionalAcademicInfo(Base):
    __tablename__ = "professional_academic_info"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    professional_id = Column(Integer, ForeignKey('professional.id'))
    title = Column(String(20))
    institution = Column(String(20))
    country = Column(String(20))
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    description = Column(String(20))