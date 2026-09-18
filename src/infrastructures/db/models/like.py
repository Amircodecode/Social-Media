from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..base import Base
from src.infrastructures.db.mixins import CommonMixin


class LikeTable(Base, CommonMixin):
    __tablename__ = "likes"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    article_id = Column(UUID, ForeignKey("articles.id"), nullable=False)
