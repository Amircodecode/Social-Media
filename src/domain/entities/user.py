import uuid
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    full_name: str
    password: str
    is_verified: bool = False
    verification_token: uuid.UUID = Field(default_factory=uuid.uuid4)
    token_expires_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(hours=24)
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {"from_attributes": True}

    @field_validator("full_name")
    @classmethod
    def lowercase_name(cls, v):
        return v.lower()
