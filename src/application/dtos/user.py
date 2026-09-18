from datetime import datetime
import uuid
from typing import List
from src.application.dtos.article import ArticleResponse
from src.application.dtos.base import Base


class UserResponse(Base):
    id: uuid.UUID
    email: str
    full_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserWithArticlesResponse(Base):
    full_name: str
    articles: List[ArticleResponse] = []
