import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserRegisterDTO(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=6, max_length=999)
    username: str = Field(min_length=6, max_length=999)
    password: str = Field(min_length=6)

class UserResponseDTO(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    username: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
        
        
class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"