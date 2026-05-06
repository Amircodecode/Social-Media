from src.domain.entities.user import User
from src.infrastructures.auth.password import hash_password
import re
from fastapi import HTTPException
import uuid


class RegisterUser:
    def __init__(self, repository):
        self.repository = repository

    async def execute(self, email, full_name, password):
        if not re.match(r"^[a-zа-яё\s]+$", full_name):
            raise HTTPException(
                status_code=400, detail="Full name must contain only lowercase letters"
            )
        if len(full_name) < 5 or len(full_name) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Full name must be between 5 and 1000 characters",
            )
        hashed_password = hash_password(password)
        token = str(uuid.uuid4())
        user = User(
            email=email,
            full_name=full_name,
            password=hashed_password,
            verification_token=token,
        )
        return await self.repository.save(user)
