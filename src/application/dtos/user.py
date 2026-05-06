from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import List
from .article import ArticleResponse


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserWithArticlesResponse(BaseModel):
    full_name: str
    articles: List[ArticleResponse] = []

    class Config:
        from_attributes = True
