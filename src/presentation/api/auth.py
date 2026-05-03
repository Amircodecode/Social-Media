from fastapi import APIRouter
from src.application.use_cases.register_user import RegisterUser
from src.infrastructures.repositories.user import UserRepository
from src.application.dtos.user import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(email: str, full_name: str, password: str):
    repository = UserRepository()
    use_case = RegisterUser(repository)
    return await use_case.execute(email, full_name, password)