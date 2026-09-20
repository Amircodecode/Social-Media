import uuid
from src.application.dtos.base import Base


class CreateCommentRequest(Base):
    content: str
    article_id: uuid.UUID
