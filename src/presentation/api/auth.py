from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.use_cases.register_user import RegisterUser
from src.application.use_cases.login_user import LoginUser
from src.application.dtos.user import RegisterRequest, UpdateUserRequest, UserResponse
from src.infrastructures.repositories.user import UserRepository
from src.infrastructures.auth.dependencies import get_current_user
from src.infrastructures.auth.password import hash_password
from src.infrastructures.db.database import get_session
from src.infrastructures.db.models.user import UserTable

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    use_case = RegisterUser(repository)
    return await use_case.execute(data)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    use_case = LoginUser(repository)
    token = await use_case.execute(form_data.username, form_data.password)
    if token:
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: UserTable = Depends(get_current_user)):
    return current_user


@router.delete("/delete")
async def delete_user(
    current_user: UserTable = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    await repository.delete(current_user.id)
    return {"message": "User deleted successfully!!"}


@router.put("/update", response_model=UserResponse)
async def update_user(
    data: UpdateUserRequest,
    current_user: UserTable = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    updated_user = await repository.update(
        current_user.id,
        email=data.email,
        full_name=data.full_name,
        password=hash_password(data.password),
    )
    return updated_user


@router.get("/verify")
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    user = await repository.find_by_verification_token(token)
    if user and user.token_expires_at > datetime.now():
        await repository.update(user.id, is_verified=True)
        return {"message": "Email verified successfully!"}
    raise HTTPException(status_code=400, detail="Invalid or expired token")
