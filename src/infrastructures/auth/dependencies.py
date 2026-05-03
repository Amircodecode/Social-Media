from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.infrastructures.auth.jwt import decode_access_token
from src.infrastructures.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    repository = UserRepository()
    user = await repository.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user