from fastapi import FastAPI
import schemas
import database
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="server_logs.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def get_root():
    return "Welcome to the books api"


@app.post("/book/")
def create_book(request: schemas.BookAuthorPayload):
    try:
        database.add_book(
            convert_into_book_db_model(request.book),
            convert_into_author_db_model(request.author),
        )
        return (
            "New book added "
            + request.book.title
            + " "
            + str(request.book.number_of_pages)
            + " New author added "
            + request.author.first_name
            + " "
            + request.author.last_name
        )
    except Exception as e:  # Catch specific exception type if possible.
        logger.error(f"An error occurred while adding a new book: {str(e)}")
        raise  # Re-raise the exception to provide proper feedback to the client.


def convert_into_book_db_model(book: schemas.Book):
    return database.Book(title=book.title, number_of_pages=book.number_of_pages)


def convert_into_author_db_model(author: schemas.Author):
    return database.Author(first_name=author.first_name, last_name=author.last_name)
