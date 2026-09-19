import uuid
from datetime import datetime
from pydantic import Field, field_validator
from src.application.dtos.base import Base


class RegisterRequest(Base):
    email: str = Field(examples=["test@gmail.com"])
    password: str = Field(min_length=8, max_length=128, examples=["password123"])
    full_name: str = Field(
        min_length=5, max_length=1000, pattern=r"^[a-zа-яё\s]+$", examples=["Jon Jones"]
    )

    @field_validator("full_name")
    @classmethod
    def lowercase_name(cls, v: str) -> str:
        return v.lower()


class UpdateUserRequest(Base):
    email: str
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=5, max_length=1000, pattern=r"^[a-zа-яё\s]+$")

    @field_validator("full_name")
    @classmethod
    def lowercase_name(cls, v: str) -> str:
        return v.lower()


class UserResponse(Base):
    id: uuid.UUID
    email: str
    full_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
