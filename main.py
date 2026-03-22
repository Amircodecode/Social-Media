from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from database import create_tables, get_db, User as UserModel
from schemas import UserSchema

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def main_menu():
    return {"server": "ready"}

@app.post("/users")
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    new_user = UserModel(email=user.email, full_name=user.full_name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user