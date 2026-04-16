from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from ..base import Base

class UserTable(Base):
    __tablename__ = "users" 

    id = Column(UUID, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    is_verified = Column(Boolean, default = False)
    full_name = Column(String, nullable = False)
    password = Column(String, nullable = False, unique = True)
    created_at = Column(DateTime, nullable = False, default = func.now())   
    updated_at = Column(DateTime, nullable = False, default = func.now())   
    