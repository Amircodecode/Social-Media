from fastapi import APIRouter
from src.application.use_cases.register_user import RegisterUser
from src.infrastructures.repositories.user import UserRepository
from src.application.dtos.user import UserResponse
from src.application.use_cases.login_user import LoginUser
from src.infrastructures.auth.dependencies import get_current_user
from src.domain.entities.user import User
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

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
    return {"message": "User deleted successfully"}