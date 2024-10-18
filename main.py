import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String)
    language = Column(String)
    
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    
    author = relationship("Author", back_populates="books")

DATABASE_URL = "postgresql+psycopg2://postgres:stagingpass@localhost:5432/book_borrowing_db"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('books.json', 'r') as file:
    books_data = json.load(file)

for book_data in books_data:
    author_name = book_data['author']
    author = session.query(Author).filter_by(name=author_name).first()
    
    if not author:
        author = Author(
            name=author_name,
            country=book_data['country'],
            language=book_data['language']
        )
        session.add(author)
        session.commit()
    
    book = Book(
        title=book_data['title'],
        year=book_data['year'],
        pages=book_data['pages'],
        author_id=author.id
    )
    session.add(book)

session.commit()

session.close()

print("Data has been successfully inserted!")
