import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructures.db.models import UserModel
from src.application.dtos.user import UserRegisterDTO, UserResponseDTO

class RegisterUserUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, data: UserRegisterDTO) -> UserResponseDTO:
        # 1. Проверяем что email не занят
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == data.email)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise ValueError("Email уже занят")

        # 2. Хэшируем пароль
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        # 3. Создаём пользователя
        new_user = UserModel(
            email=data.email,
            full_name=data.full_name,
            username=data.username,
            password=hashed.decode()
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return UserResponseDTO.model_validate(new_user)