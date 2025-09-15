"""
Seeds sample authors and books with valid 10-digit ISBNs.

Usage:
    python scripts/seed.py
"""
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Author, Book

AUTHORS = [
    {"name": "J. R. R. Tolkien", "email": "tolkien@example.com"},
    {"name": "George R. R. Martin", "email": "grrm@example.com"},
    {"name": "Harper Lee", "email": "harper.lee@example.com"},
    {"name": "Jane Austen", "email": "jane.austen@example.com"},
    {"name": "Agatha Christie", "email": "agatha@example.com"},
]

# 10-digit-only ISBNs (no dashes/spaces/letters) – intentionally simple placeholders
BOOKS = [
    {"title": "The Hobbit", "isbn": "1234567890", "published_year": 1937, "author": "J. R. R. Tolkien"},
    {"title": "The Lord of the Rings", "isbn": "1111111111", "published_year": 1954, "author": "J. R. R. Tolkien"},
    {"title": "A Game of Thrones", "isbn": "2222222222", "published_year": 1996, "author": "George R. R. Martin"},
    {"title": "A Clash of Kings", "isbn": "3333333333", "published_year": 1998, "author": "George R. R. Martin"},
    {"title": "To Kill a Mockingbird", "isbn": "4444444444", "published_year": 1960, "author": "Harper Lee"},
    {"title": "Pride and Prejudice", "isbn": "5555555555", "published_year": 1813, "author": "Jane Austen"},
    {"title": "Murder on the Orient Express", "isbn": "6666666666", "published_year": 1934, "author": "Agatha Christie"},
    {"title": "Emma", "isbn": "7777777777", "published_year": 1815, "author": "Jane Austen"},
    {"title": "The Silmarillion", "isbn": "8888888888", "published_year": 1977, "author": "J. R. R. Tolkien"},
    {"title": "And Then There Were None", "isbn": "9999999999", "published_year": 1939, "author": "Agatha Christie"},
]

def main():
    db = SessionLocal()
    try:
        # prevent duplicate seeding by checking an author count
        existing = db.execute(select(Author)).scalars().first()
        if existing:
            print("Database already has data; skipping seed.")
            return

        # insert authors
        author_map = {}
        for a in AUTHORS:
            author = Author(name=a["name"], email=a["email"])
            db.add(author)
            db.flush()  # get id
            author_map[a["name"]] = author.id

        # insert books
        for b in BOOKS:
            db.add(Book(
                title=b["title"],
                isbn=b["isbn"],
                published_year=b["published_year"],
                author_id=author_map[b["author"]],
            ))

        db.commit()
        print("Seeded authors and books.")
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
