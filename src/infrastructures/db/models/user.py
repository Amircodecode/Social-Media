from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from ..base import Base

class UserTable(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    is_verified = Column(Boolean, default = False)
    full_name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(DateTime, nullable = False)   
    updated_at = Column(DateTime, nullable = False)   
    