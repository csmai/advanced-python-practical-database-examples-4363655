from fastapi import FastAPI
import schemas
import database

app = FastAPI()


@app.get("/")
def get_root():
    return "Welcome to the books api"


@app.post("/book/")
def create_book(request: schemas.BookAuthorPayload):
    database.add_book(
        conv_payload_to_Author(request.author), conv_payload_to_Book(request.book)
    )
    return f"""New Book to add: {request.book.title} with {str(request.book.number_of_pages)} pages. Author: {request.author.first_name} {request.author.last_name}"""


def conv_payload_to_Book(book_pl):
    return database.Book(title=book_pl.title, number_of_pages=book_pl.number_of_pages)


def conv_payload_to_Author(author_pl):
    return database.Author(
        first_name=author_pl.first_name, last_name=author_pl.last_name
    )
