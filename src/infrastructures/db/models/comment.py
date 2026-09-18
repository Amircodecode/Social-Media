from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..base import Base
from src.infrastructures.db.mixins import CommonMixin


class CommentTable(Base, CommonMixin):
    __tablename__ = "comments"

    article_id = Column(UUID, ForeignKey("articles.id"), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
