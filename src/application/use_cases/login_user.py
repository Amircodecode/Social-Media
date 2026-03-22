import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructures.db.models import UserModel
from src.infrastructures.auth.jwt import create_access_token, create_refresh_token
from src.application.dtos.user import UserLoginDTO, TokenResponseDTO

class LoginUserUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, data: UserLoginDTO) -> TokenResponseDTO:
        # 1. Ищем пользователя по email
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == data.email)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError("Неверный email или пароль")

        # 2. Проверяем пароль
        if not bcrypt.checkpw(data.password.encode(), user.password.encode()):
            raise ValueError("Неверный email или пароль")

        # 3. Создаём токены
        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))

        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )