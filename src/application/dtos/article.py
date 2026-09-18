from datetime import datetime
import uuid
from src.application.dtos.base import Base


class ArticleResponse(Base):
    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
