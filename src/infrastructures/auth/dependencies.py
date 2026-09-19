from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructures.auth.jwt import decode_access_token
from src.infrastructures.repositories.user import UserRepository
from src.infrastructures.db.database import get_session
from src.infrastructures.db.models.user import UserTable
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> UserTable:
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user_id = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    repository = UserRepository(session)
    user = await repository.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
