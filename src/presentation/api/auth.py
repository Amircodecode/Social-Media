from src.application.use_cases.register_user import RegisterUser
from src.infrastructures.repositories.user import UserRepository
from src.application.dtos.user import UserResponse
from src.application.use_cases.login_user import LoginUser
from src.infrastructures.auth.dependencies import get_current_user
from src.domain.entities.user import User
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.infrastructures.auth.password import hash_password
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(email: str, full_name: str, password: str):
    repository = UserRepository()
    use_case = RegisterUser(repository)
    return await use_case.execute(email, full_name, password)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    repository = UserRepository()
    use_case = LoginUser(repository)
    token = await use_case.execute(form_data.username, form_data.password)
    if token:
        return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/delete")
async def delete_user(current_user: User = Depends(get_current_user)):
    repository = UserRepository()
    await repository.delete(current_user.id)
    return {"message": "User deleted successfully!!"}


@router.put("/update", response_model=UserResponse)
async def update_user(
    email: str,
    full_name: str,
    password: str,
    current_user: User = Depends(get_current_user),
):
    repository = UserRepository()
    current_user.email = email
    current_user.full_name = full_name
    current_user.password = hash_password(password)
    updated_user = await repository.update(current_user)
    return updated_user


@router.get("/verify")
async def verify_email(token: str):
    repository = UserRepository()
    user = await repository.find_by_verification_token(token)
    if user and user.token_expires_at > datetime.now():
        user.is_verified = True
        await repository.update(user)
        return {"message": "Email verified successfully!"}
    return {"error": "Invalid or expired token"}
