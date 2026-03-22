from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructures.db.database import get_db
from src.application.dtos.user import UserRegisterDTO, UserResponseDTO
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.login_user import LoginUserUseCase
from src.application.dtos.user import UserRegisterDTO, UserResponseDTO, UserLoginDTO, TokenResponseDTO
from src.infrastructures.auth.dependencies import get_current_user
from src.infrastructures.db.models import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponseDTO, status_code=201)
async def register(data: UserRegisterDTO, db: AsyncSession = Depends(get_db)):
    try:
        use_case = RegisterUserUseCase(db)
        return await use_case.execute(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/login", response_model=TokenResponseDTO)
async def login(data: UserLoginDTO, db: AsyncSession = Depends(get_db)):
    try:
        use_case = LoginUserUseCase(db)
        return await use_case.execute(data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.get("/me", response_model=UserResponseDTO)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user