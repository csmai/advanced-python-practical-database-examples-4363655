from pydantic import BaseModel


class Author(BaseModel):
    first_name: str
    last_name: str


class Book(BaseModel):
    title: str
    number_of_pages: int


class BookAuthorPayload(BaseModel):
    author: Author
    book: Book
