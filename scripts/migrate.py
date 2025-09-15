"""
Creates SQLite schema for authors and books.

Usage:
    python scripts/migrate.py
"""
from app.db import engine
from app.models import Base

def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    main()
