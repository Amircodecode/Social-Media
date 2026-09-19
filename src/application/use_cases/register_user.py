import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException
from src.infrastructures.auth.password import hash_password
from src.application.dtos.user import RegisterRequest
from src.infrastructures.repositories.user import UserRepository


class RegisterUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, data: RegisterRequest):
        existing = await self.repository.find_by_email(data.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

        hashed_password = hash_password(data.password)
        verification_token = uuid.uuid4()
        token_expires_at = datetime.now() + timedelta(hours=24)

        return await self.repository.create(
            email=data.email,
            full_name=data.full_name,
            password=hashed_password,
            verification_token=verification_token,
            token_expires_at=token_expires_at,
        )
