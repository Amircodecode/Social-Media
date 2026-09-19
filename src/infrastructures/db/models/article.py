from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..base import Base
from src.infrastructures.db.mixins import CommonMixin


class ArticleTable(Base, CommonMixin):
    __tablename__ = "articles"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)

    user = relationship("UserTable", back_populates="articles")
