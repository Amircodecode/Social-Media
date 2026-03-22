from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructures.db.database import create_tables
from src.presentation.api.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"status": "ok"}