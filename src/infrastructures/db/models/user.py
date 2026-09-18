from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.infrastructures.db.base import Base
from src.infrastructures.db.mixins import CommonMixin


class UserTable(Base, CommonMixin):
    __tablename__ = "users"

    verification_token = Column(UUID, unique=True, nullable=False)
    token_expires_at = Column(DateTime, nullable=True)
    email = Column(String, unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
