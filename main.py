from fastapi import FastAPI
app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message":"hello"}

@app.get("/")
def main_menu():
    return {"server":"ready"}

@app.get("/about")
def about():
    return {"name":"amir"}