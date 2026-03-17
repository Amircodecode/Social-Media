from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, get_db, User as UserModel
from pydantic import BaseModel, Field, EmailStr
from fastapi import Depends


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()  # выполняется при старте сервера
    yield                  # сервер работает
                          # после yield — выполняется при остановке

app = FastAPI(lifespan=lifespan)

class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0, le=120)
    email: EmailStr


fake_items = [
    {
        "item_name": "apple"
    },
    {
        "item_name": "banana"
    },
    {
        "item_name": "pineapple"
    }
]

@app.get("/hello")
def say_hello():
    return {"message":"hello"}

@app.get("/")
def main_menu():
    return {"server":"ready"}

@app.get("/about")
def about():
    return {"name":"amir"}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q:str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/search") 
def search(name: str, age: int):
    return {"name": name, "age": age}


@app.get("/user/{user_id}") 
def get_user(user_id: int):
    return {"user_id": user_id} # path parametr 

# @app.get("/search") #query
# def search(name: str):
#     return {"name": name}

@app.get("/gandon")
def gandon(name: str, age: int, dildo: int, girl: str):
    return {"name": name, "age": age, "dildo": dildo, "girl": girl}

@app.post("/register")
async def register(user: User):
    return {"message": "user created","received": user}

@app.post("/users")
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    # db — это сессия, готова к работе
    pass