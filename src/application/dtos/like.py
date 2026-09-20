import uuid
from src.application.dtos.base import Base


class CreateLikeRequest(Base):
    article_id: uuid.UUID
