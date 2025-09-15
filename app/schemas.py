from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.utils.validation import is_valid_isbn10, is_valid_year

#AUTHOR SCHEMAS
class AuthorCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr

class AuthorOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    book_count: int | None = 0
    class Config: from_attributes = True

class BookOut(BaseModel):
    id: int
    title: str
    isbn: str
    published_year: int | None
    author_id: int
    created_at: datetime
    class Config: from_attributes = True

class AuthorWithBooks(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    books: list[BookOut] = []
    class Config: from_attributes = True


#BOOK SCHEMAS


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    isbn: str
    published_year: int | None = None
    author_id: int
    @field_validator("isbn")
    @classmethod
    def _v_isbn(cls, v): 
        if not is_valid_isbn10(v): 
            raise ValueError("ISBN must be exactly 10 digits.")
        return v
    
    @field_validator("published_year")
    @classmethod
    def _v_year(cls, v):
        if not is_valid_year(v): 
            raise ValueError("Published year must be between 1000 and 2100.")
        return v

class BookUpdate(BaseModel):
    title: str | None = None
    isbn: str | None = None
    published_year: int | None = None
    author_id: int | None = None
    @field_validator("isbn")
    @classmethod
    def _vu_isbn(cls, v):
        if v is not None and not is_valid_isbn10(v): 
            raise ValueError("ISBN must be exactly 10 digits.")
        return v
    
    @field_validator("published_year")
    @classmethod
    def _vu_year(cls, v):
        if v is not None and not is_valid_year(v): 
            raise ValueError("Published year must be between 1000 and 2100.")
        return v

class BookOut(BaseModel):
    id: int; title: str; isbn: str; published_year: int | None; author_id: int
    created_at: datetime
    class Config: from_attributes = True

class BookWithAuthor(BookOut):
    author: AuthorOut  # uses AuthorOut defined above
