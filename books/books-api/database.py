from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, select
import os

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


def add_book(author: Author, book: Book):
    with Session(engine) as session:
        # Check if the book already exists
        existing_book = session.execute(
            select(Book).filter_by(
                title=book.title, number_of_pages=book.number_of_pages
            )
        ).scalar()
        if existing_book is not None:
            print("Book already exists.")
            return

        # Check if the author already exists
        existing_author = session.execute(
            select(Author).filter_by(
                first_name=author.first_name, last_name=author.last_name
            )
        ).scalar()

        # Add an author if needed
        if existing_author is not None:
            print("Author already added. Adding Book.")
        else:
            print("Adding Author")
            session.add(author)
            print("Author added")
            session.flush()

        # Add th ebook
        session.add(book)
        print("Book added")
        session.flush()

        # Add the pair to the bookauthors table
        pairing = BookAuthor(author_id=author.author_id, book_id=book.book_id)
        session.add(pairing)
        print(f"Book-Author pair added")
        session.commit()
