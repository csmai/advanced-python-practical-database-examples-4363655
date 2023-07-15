from fastapi import FastAPI
import schemas

app = FastAPI()


@app.get("/")
def get_root():
    return "Welcome to the books api"


@app.post("/book/")
def create_book(request: schemas.BookAuthorPayload):
    return f"""New Book to add: {request.book.title} with {str(request.book.number_of_pages)} pages. Author: {request.author.first_name} {request.author.last_name}"""
