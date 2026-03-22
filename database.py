from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import uuid

# 1. URL базы данных
DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/socialnet"

# 2. Создание движка
engine = create_async_engine(DATABASE_URL)

# 3. Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# 4. Модель пользователя
class User(Base):
    __tablename__ = "users"

    # Используем String(36) или тип UUID для совместимости
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

# 5. Функция создания таблиц
async def create_tables():
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)

# 6. Настройка фабрики сессий
# expire_on_commit=False критически важно для асинхронности!
AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 7. Dependency для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()