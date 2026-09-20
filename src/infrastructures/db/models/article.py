from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..base import Base
from src.infrastructures.db.mixins import CommonMixin


class ArticleTable(Base, CommonMixin):
    __tablename__ = "articles"

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)

    user = relationship("UserTable", back_populates="articles")
