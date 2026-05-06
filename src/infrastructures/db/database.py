from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .base import Base

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/socialnet"

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
