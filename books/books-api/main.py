from fastapi import FastAPI
import schemas
import database
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="server_logs.log",
)


@app.get("/")
def get_root():
    return "Welcome to the books api"


@app.post("/book/")
def create_book(request: schemas.BookAuthorPayload):
    try:
        author = conv_payload_to_Author(request.author)
        book = conv_payload_to_Book(request.book)

        # Log the book and author details
        logging.info("Adding Book: %s with %d pages.", book.title, book.number_of_pages)
        logging.info("Adding Author: %s %s", author.first_name, author.last_name)

        database.add_book(author, book)

        response_msg = f"""New Book added: {book.title} with {str(book.number_of_pages)} pages. Author: {author.first_name} {author.last_name}"""
        logging.info(response_msg)
        return response_msg
    except Exception as e:
        # Log any exceptions that occur during book creation
        logging.error("Error adding book: %s", str(e))
        return "Failed to add book. Please check the server logs for details."


def conv_payload_to_Book(book_pl: schemas.Book):
    return database.Book(title=book_pl.title, number_of_pages=book_pl.number_of_pages)


def conv_payload_to_Author(author_pl: schemas.Author):
    return database.Author(
        first_name=author_pl.first_name, last_name=author_pl.last_name
    )
