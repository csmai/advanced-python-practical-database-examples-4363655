from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, select, and_
import os
import logging

password = os.getenv("P4PASSWD")

engine = create_engine(
    f"mysql+mysqlconnector://root:{password}@localhost:3306/books", echo=True
)

mapper_registry = registry()

Base = mapper_registry.generate_base()


class Author(Base):
    __tablename__ = "authors"
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))

    def __repr__(self):
        return "<Author(author_id='{0}', first_name='{1}', last_name='{2}')>".format(
            self.author_id, self.first_name, self.last_name
        )


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    title = Column(String(length=255))
    number_of_pages = Column(Integer)

    def __repr__(self):
        return "<Book(book_id='{0}', title='{1}', number_of_pages='{2}')>".format(
            self.book_id, self.title, self.number_of_pages
        )


class BookAuthor(Base):
    __tablename__ = "bookauthors"

    bookauthor_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.author_id"))
    book_id = Column(Integer, ForeignKey("books.book_id"))

    author = relationship("Author")
    book = relationship("Book")

    def __repr__(self):
        return "<BookAuthor (bookauthor_id='{0}', author_id='{1}', book_id='{2}', first_name='{3}', last_name='{4}', title='{5}')>".format(
            self.bookauthor_id,
            self.author_id,
            self.book_id,
            self.author.first_name,
            self.author.last_name,
            self.book.title,
        )


Base.metadata.create_all(engine)


def add_book(book: Book, author: Author):
    with Session(engine) as session:
        logging.info(
            "Check if the book already exist %s %s", book.title, book.number_of_pages
        )
        existing_book = session.execute(
            select(Book).filter_by(
                title=book.title, number_of_pages=book.number_of_pages
            )
        ).scalar()

        logging.info(
            "Check if the book already exist. Existing book: %s", existing_book
        )

        if existing_book is not None:
            logging.info("Book already exists.")
            return

        logging.info("Add the book")
        session.add(book)
        logging.info("Book added")

        logging.info(
            "Check if the author already exists %s %s",
            author.first_name,
            author.last_name,
        )

        existing_author = session.execute(
            select(Author).filter_by(
                first_name=author.first_name, last_name=author.last_name
            )
        ).scalar()

        logging.info("Add an author if needed")
        if existing_author is not None:
            logging.info("Author already added. Adding Book.")
            author_id = existing_author.author_id
        else:
            logging.info("Adding Author")
            session.add(author)
            logging.info("Author added")
            session.flush()
            author_id = author.author_id

        # Add the pair to the bookauthors table
        pairing = BookAuthor(author_id=author_id, book_id=book.book_id)
        session.add(pairing)
        logging.info("Book-Author pair added")
        session.commit()


def get_book_author_data(given_id):
    with Session(engine) as session:
        logging.info("Getting the book's data with id:%s", given_id)

        found_data = session.execute(
            select(Book, Author)
            .select_from(BookAuthor)
            .join(Book, Book.book_id == given_id)
            .join(Author, Author.author_id == BookAuthor.author_id)
        ).first()

        if found_data:
            found_book, found_author = found_data
            logging.info(
                "Getting the book data title: %s, number of pages: %s",
                found_book.title,
                found_book.number_of_pages,
            )
            logging.info(
                "Getting the author data %s %s",
                found_author.first_name,
                found_author.last_name,
            )
            return found_book, found_author

    return None
