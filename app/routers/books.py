from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.deps import get_db
from app import schemas
from app.crud import create_book, get_book_by_id, update_book, list_books_paginated, count_books
from app.models import Author, Book

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("", response_model=list[schemas.BookOut])
@router.get("")
def get_books(
    title: str | None = None,
    author: str | None = None,
    year: int | None = None,
    sort: str | None = Query(default=None, description="title|published_year|created_at"),
    order: str | None = Query(default="asc", regex="(?i)^(asc|desc)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    total = count_books(db, title=title, author=author, year=year)
    items = list_books_paginated(db, title=title, author=author, year=year, sort=sort, order=order, limit=limit, offset=offset)
    return {"data": items, "total": total, "limit": limit, "offset": offset}

@router.post("", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    if not db.get(Author, payload.author_id):
        raise HTTPException(status_code=400, detail="Invalid author_id. Author does not exist.")
    if db.execute(select(Book).where(Book.isbn == payload.isbn)).scalars().first():
        raise HTTPException(status_code=409, detail="ISBN already exists.")
    return create_book(db, payload)

@router.get("/{book_id}", response_model=schemas.BookWithAuthor)
def get_book(book_id: int, db: Session = Depends(get_db)):
    b = get_book_by_id(db, book_id)
    if not b: raise HTTPException(status_code=404, detail="Book not found.")
    return b

@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book_endpoint(book_id: int, payload: schemas.BookUpdate, db: Session = Depends(get_db)):
    b = get_book_by_id(db, book_id)
    if not b: raise HTTPException(status_code=404, detail="Book not found.")
    return update_book(db, b, payload)
