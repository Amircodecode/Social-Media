import uuid
from datetime import datetime
from pydantic import Field, field_validator, EmailStr
from src.application.dtos.base import Base


class RegisterRequest(Base):
    email: EmailStr = Field(examples=["string"])
    password: str = Field(min_length=8, max_length=128, examples=["string"])
    full_name: str = Field(
        min_length=5, max_length=1000, pattern=r"^[a-zа-яё\s]+$", examples=["string"]
    )

    @field_validator("full_name", mode="before")
    @classmethod
    def lowercase_name(cls, v: str) -> str:
        return v.lower() if isinstance(v, str) else v


class UpdateUserRequest(Base):
    email: EmailStr = Field(examples=["string"])
    password: str = Field(min_length=8, max_length=128, examples=["string"])
    full_name: str = Field(
        min_length=5, max_length=1000, pattern=r"^[a-zа-яё\s]+$", examples=["string"]
    )

    @field_validator("full_name", mode="before")
    @classmethod
    def lowercase_name(cls, v: str) -> str:
        return v.lower() if isinstance(v, str) else v


class UserResponse(Base):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
