from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.user_service import UserService
from src.application.dtos.user import RegisterRequest, UpdateUserRequest, UserResponse
from src.infrastructures.repositories.user import UserRepository
from src.infrastructures.auth.dependencies import get_current_user
from src.infrastructures.db.database import get_session
from src.infrastructures.db.models.user import UserTable

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    data: RegisterRequest, service: UserService = Depends(get_user_service)
):
    return await service.register(data)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    token = await service.login(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: UserTable = Depends(get_current_user)):
    return current_user


@router.delete("/delete")
async def delete_user(
    current_user: UserTable = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    await service.delete(current_user.id)
    return {"message": "User deleted successfully!!"}


@router.put("/update", response_model=UserResponse)
async def update_user(
    data: UpdateUserRequest,
    current_user: UserTable = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.update(current_user.id, data)


@router.get("/verify")
async def verify_email(token: str, service: UserService = Depends(get_user_service)):
    if await service.verify_email(token):
        return {"message": "Email verified successfully!"}
    raise HTTPException(status_code=400, detail="Invalid or expired token")
