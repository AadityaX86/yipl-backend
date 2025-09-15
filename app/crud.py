from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc, desc
from app.models import Author, Book
from app.schemas import AuthorCreate
from app.schemas import BookCreate, BookUpdate

def create_author(db: Session, author_in: AuthorCreate) -> Author:
    author = Author(name=author_in.name, email=author_in.email)
    db.add(author); db.commit(); db.refresh(author)
    return author

def get_author_by_id(db: Session, author_id: int) -> Optional[Author]:
    return db.get(Author, author_id)

def list_authors(db: Session, name: Optional[str], sort: Optional[str], order: Optional[str]) -> list[tuple[Author,int]]:
    stmt = (select(Author, func.count(Book.id).label("book_count"))
            .join(Book, Book.author_id==Author.id, isouter=True)
            .group_by(Author.id))
    if name:
        stmt = stmt.where(Author.name.ilike(f"%{name}%"))
    if sort == "book_count":
        stmt = stmt.order_by((asc if (order or "desc").lower()=="asc" else desc)("book_count"), Author.id.asc())
    else:
        stmt = stmt.order_by(Author.id.asc())
    return db.execute(stmt).all()


def create_book(db: Session, book_in: BookCreate) -> Book:
    b = Book(**book_in.dict()); db.add(b); db.commit(); db.refresh(b); return b

def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    return db.get(Book, book_id)

def update_book(db: Session, db_book: Book, updates: BookUpdate) -> Book:
    for k, v in updates.dict(exclude_unset=True).items(): setattr(db_book, k, v)
    db.add(db_book); db.commit(); db.refresh(db_book); return db_book

def list_books(db: Session, title: Optional[str], author: Optional[str], year: Optional[int], sort: Optional[str], order: Optional[str]):
    stmt = select(Book).join(Book.author)
    if title:  stmt = stmt.where(Book.title.ilike(f"%{title}%"))
    if author: stmt = stmt.where(Author.name.ilike(f"%{author}%"))
    if year:   stmt = stmt.where(Book.published_year == year)
    if sort == "title":
        stmt = stmt.order_by(Book.title.asc() if (order or "asc")=="asc" else Book.title.desc())
    elif sort == "published_year":
        stmt = stmt.order_by(Book.published_year.asc() if (order or "asc")=="asc" else Book.published_year.desc())
    elif sort == "created_at":
        stmt = stmt.order_by(Book.created_at.asc() if (order or "asc")=="asc" else Book.created_at.desc())
    else:
        stmt = stmt.order_by(Book.id.asc())
    return db.execute(stmt).scalars().all()



#pagination starts

# AUTHORS with pagination 
def count_authors(db: Session, name: Optional[str]) -> int:
    stmt = select(func.count(Author.id))
    if name:
        stmt = stmt.where(Author.name.ilike(f"%{name}%"))
    return db.execute(stmt).scalar_one()

def list_authors_paginated(
    db: Session,
    name: Optional[str],
    sort: Optional[str],
    order: Optional[str],
    limit: int,
    offset: int,
) -> List[Tuple[Author, int]]:
    stmt = (
        select(Author, func.count(Book.id).label("book_count"))
        .join(Book, Book.author_id == Author.id, isouter=True)
        .group_by(Author.id)
    )
    if name:
        stmt = stmt.where(Author.name.ilike(f"%{name}%"))

    if sort == "book_count":
        ordering = asc("book_count") if (order or "desc").lower() == "asc" else desc("book_count")
        stmt = stmt.order_by(ordering, Author.id.asc())
    else:
        stmt = stmt.order_by(Author.id.asc())

    stmt = stmt.limit(limit).offset(offset)
    return db.execute(stmt).all()

# BOOKS with pagination 
def count_books(db: Session, title: Optional[str], author: Optional[str], year: Optional[int]) -> int:
    stmt = select(func.count(Book.id)).join(Book.author)
    if title:
        stmt = stmt.where(Book.title.ilike(f"%{title}%"))
    if author:
        stmt = stmt.where(Author.name.ilike(f"%{author}%"))
    if year:
        stmt = stmt.where(Book.published_year == year)
    return db.execute(stmt).scalar_one()

def list_books_paginated(
    db: Session,
    title: Optional[str],
    author: Optional[str],
    year: Optional[int],
    sort: Optional[str],
    order: Optional[str],
    limit: int,
    offset: int,
):
    stmt = select(Book).join(Book.author)
    if title:
        stmt = stmt.where(Book.title.ilike(f"%{title}%"))
    if author:
        stmt = stmt.where(Author.name.ilike(f"%{author}%"))
    if year:
        stmt = stmt.where(Book.published_year == year)

    if sort == "title":
        stmt = stmt.order_by(Book.title.asc() if (order or "asc").lower()=="asc" else Book.title.desc())
    elif sort == "published_year":
        stmt = stmt.order_by(Book.published_year.asc() if (order or "asc").lower()=="asc" else Book.published_year.desc())
    elif sort == "created_at":
        stmt = stmt.order_by(Book.created_at.asc() if (order or "asc").lower()=="asc" else Book.created_at.desc())
    else:
        stmt = stmt.order_by(Book.id.asc())

    stmt = stmt.limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()