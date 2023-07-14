from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get():
    return "Welcome to my app!"
