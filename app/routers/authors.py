from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.deps import get_db
from app import schemas
from app.crud import create_author, get_author_by_id, list_authors_paginated, count_authors

from app.models import Author

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("")
def get_authors(
    name: str | None = Query(default=None),
    sort: str | None = Query(default=None, description='use "book_count"'),
    order: str | None = Query(default="desc", regex="(?i)^(asc|desc)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    total = count_authors(db, name=name)
    rows = list_authors_paginated(db, name=name, sort=sort, order=order, limit=limit, offset=offset)
    data = [schemas.AuthorOut(
        id=a.id, name=a.name, email=a.email, created_at=a.created_at, book_count=bc or 0
    ) for a, bc in rows]
    return {"data": data, "total": total, "limit": limit, "offset": offset}

@router.post("", response_model=schemas.AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author_endpoint(payload: schemas.AuthorCreate, db: Session = Depends(get_db)):
    if db.execute(select(Author).where(Author.email==payload.email)).scalars().first():
        raise HTTPException(status_code=409, detail="Email already exists.")
    a = create_author(db, payload)
    return schemas.AuthorOut(id=a.id, name=a.name, email=a.email, created_at=a.created_at, book_count=0)

@router.get("/{author_id}", response_model=schemas.AuthorWithBooks)
def get_author(author_id: int, db: Session = Depends(get_db)):
    a = get_author_by_id(db, author_id)
    if not a:
        raise HTTPException(status_code=404, detail="Author not found.")
    return a
