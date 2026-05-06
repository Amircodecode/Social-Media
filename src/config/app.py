from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.infrastructures.db.database import create_tables
from src.presentation.api.auth import router as auth_router
from src.presentation.api.posts import router as posts_router
from src.presentation.api.comments import router as comments_router
from src.presentation.api.like import router as likes_router
from src.infrastructures.db.database import SessionLocal
from src.infrastructures.db.models.user import UserTable
from src.infrastructures.db.models.article import ArticleTable
from sqlalchemy import delete
from datetime import datetime


async def delete_unverified_users():
    async with SessionLocal() as session:
        await session.execute(
            delete(UserTable).where(
                ~UserTable.is_verified,
                UserTable.token_expires_at < datetime.now(),
            )
        )
        await session.commit()


async def delete_old_articles():
    async with SessionLocal() as session:
        await session.execute(delete(ArticleTable))
        await session.commit()


scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    scheduler.add_job(delete_unverified_users, "interval", days=1)
    scheduler.add_job(delete_old_articles, "interval", days=30)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)
