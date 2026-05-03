from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructures.db.database import create_tables
from src.presentation.api.auth import router as auth_router
from src.presentation.api.posts import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(posts_router)