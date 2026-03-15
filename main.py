from fastapi import FastAPI
app = FastAPI()

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
    return {"user_id": user_id}