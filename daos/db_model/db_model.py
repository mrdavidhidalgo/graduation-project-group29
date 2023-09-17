from sqlalchemy import Boolean, Column, Integer, String, DateTime
import datetime

from .database import Base

class User(Base):
    __tablename__ = "user"
    
    username = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    password = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(String(20), primary_key=True, index=True)
    