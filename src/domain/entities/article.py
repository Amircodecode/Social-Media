import uuid
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import re


class Article(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {"from_attributes": True}

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not (5 < len(v) < 1000):
            raise ValueError("Title must be between 5 and 1000 characters")
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s]+$", v):
            raise ValueError("Title must contain only latin/cyrillic letters")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if len(v) >= 10_000:
            raise ValueError("Content must be less than 10000 characters")
        return v
