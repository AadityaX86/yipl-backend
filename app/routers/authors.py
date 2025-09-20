from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.deps import get_db
from app import schemas
from app.crud import create_author, get_author_by_id, list_authors_paginated, count_authors
from app.models import Author

router = APIRouter(prefix="/authors", tags=["Authors"])

# -------------------------------
# GET /authors - List authors
# -------------------------------
@router.get("/", response_model=schemas.PaginatedAuthors)
def get_authors(
    name: str | None = Query(default=None, description="Filter by author name"),
    sort: str | None = Query(default=None, description='Sort by "book_count"'),
    order: str | None = Query(default="desc", regex="(?i)^(asc|desc)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    try:
        total = count_authors(db, name=name)
        rows = list_authors_paginated(db, name=name, sort=sort, order=order, limit=limit, offset=offset)
        
        # Ensure rows are tuples (Author, book_count)
        data = [
            schemas.AuthorOut(
                id=a.id,
                name=a.name,
                email=a.email,
                created_at=a.created_at,
                book_count=bc or 0
            ) for a, bc in rows
        ]

        return {"data": data, "total": total, "limit": limit, "offset": offset}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")


# -------------------------------
# POST /authors - Create author
# -------------------------------
@router.post("/", response_model=schemas.AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author_endpoint(payload: schemas.AuthorCreate, db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        existing_author = db.execute(select(Author).where(Author.email == payload.email)).scalars().first()
        if existing_author:
            raise HTTPException(status_code=409, detail="Email already exists.")

        a = create_author(db, payload)
        return schemas.AuthorOut(
            id=a.id,
            name=a.name,
            email=a.email,
            created_at=a.created_at,
            book_count=0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")


# -------------------------------
# GET /authors/{author_id} - Get single author
# -------------------------------
@router.get("/{author_id}", response_model=schemas.AuthorWithBooks)
def get_author(author_id: int, db: Session = Depends(get_db)):
    try:
        a = get_author_by_id(db, author_id)
        if not a:
            raise HTTPException(status_code=404, detail="Author not found.")
        return a
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
