from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession



DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/socialnet"

engine = create_async_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True)
    full_name: Mapped[str] = mapped_column(String)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    
async def create_tables():
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)
        
        
        
# Фабрика сессий — создаёт новую сессию по запросу
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency — FastAPI вызывает это автоматически для каждого запроса
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session       
