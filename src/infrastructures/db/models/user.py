from sqlalchemy import Column, String, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.infrastructures.db.base import Base
from src.infrastructures.db.mixins import CommonMixin


class UserTable(Base, CommonMixin):
    __tablename__ = "users"

    verification_token = Column(UUID(as_uuid=True), unique=True, nullable=False)
    token_expires_at = Column(DateTime, nullable=True)
    email = Column(String, unique=True, nullable=False)
    is_verified = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    articles = relationship(
        "ArticleTable", back_populates="user", cascade="all, delete-orphan"
    )
