import uuid
from datetime import datetime
from pydantic import Field
from src.application.dtos.base import Base


class CreateArticleRequest(Base):
    title: str = Field(
        min_length=5,
        max_length=1000,
        pattern=r"^[a-zA-Zа-яА-Я\s]+$",
        examples=["string"],
    )
    content: str = Field(max_length=1000, examples=["string"])


class UpdateArticleRequest(Base):
    title: str = Field(
        min_length=5,
        max_length=1000,
        pattern=r"^[a-zA-Zа-яА-Я\s]+$",
        examples=["string"],
    )
    content: str = Field(max_length=1000, examples=["string"])


class ArticleResponse(Base):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
