import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException

from src.infrastructures.repositories.user import UserRepository
from src.infrastructures.auth.password import hash_password, verify_password
from src.infrastructures.auth.jwt import create_access_token
from src.infrastructures.mail.mailer import send_verification_email
from src.application.dtos.user import RegisterRequest, UpdateUserRequest


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, data: RegisterRequest):
        existing = await self.user_repository.find_by_email(data.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

        hashed_password = hash_password(data.password)
        verification_token = uuid.uuid4()
        token_expires_at = datetime.now() + timedelta(hours=24)

        user = await self.user_repository.create(
            email=data.email,
            full_name=data.full_name,
            password=hashed_password,
            verification_token=verification_token,
            token_expires_at=token_expires_at,
        )

        await send_verification_email(user.email, user.verification_token)
        return user

    async def login(self, email: str, password: str) -> str | None:
        user = await self.user_repository.find_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return create_access_token({"sub": str(user.id)})

    async def verify_email(self, token):
        user = await self.user_repository.find_by_verification_token(token)
        if user and user.token_expires_at > datetime.now():
            await self.user_repository.update(user.id, is_verified=True)
            return True
        return False

    async def update(self, user_id, data: UpdateUserRequest):
        return await self.user_repository.update(
            user_id,
            email=data.email,
            full_name=data.full_name,
            password=hash_password(data.password),
        )

    async def delete(self, user_id):
        await self.user_repository.delete(user_id)
