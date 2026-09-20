from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from ..base import Base
from src.infrastructures.db.mixins import CommonMixin


class LikeTable(Base, CommonMixin):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="uq_like_user_article"),
    )

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    article_id = Column(
        UUID(as_uuid=True),
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
    )
