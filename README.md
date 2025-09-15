# 📚 YIPL Library Management API

A RESTful API built with **FastAPI** and **SQLite** for managing authors and books.  
This project is part of the **YIPL Internship Task 2025**.

---

## 🚀 Features

- **Authors CRUD**
  - Create, list, and fetch authors
  - Filter by name, sort by number of books
  - Pagination support (`limit`, `offset`)
- **Books CRUD**
  - Create, update, list, and fetch books
  - Filter by title, author name, or year
  - Sort by title, published year, or created date
  - Pagination support
- **Relations**
  - Each author can have many books
  - Each book belongs to one author
- **Validation**
  - Author name ≥ 2 characters
  - Valid email format
  - Book title ≥ 1 character
  - ISBN = exactly 10 digits (no spaces/dashes/letters)
  - Published year between 1000–2100
- **Error Handling**
  - Unified JSON error responses (`{ "error": "..." }`)
  - 400 for validation errors
  - 404 for not found
  - 409 for conflicts (duplicate email/ISBN)
- **Documentation**
  - Auto-generated Swagger at `/docs`
  - ReDoc at `/redoc`
- **Extras**
  - Request logging middleware
  - SQLite migration + seeding scripts
  - Dockerfile for containerized runs
  - GitHub Actions CI with pytest tests and lint

---

## 🛠️ Setup Instructions

### 1. Clone Repository
```bash
https://github.com/SamipSGz/yipl-backend-2025.git
cd yipl-backend-2025
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 📂 Database
Run migrations:
```bash
python -m scripts.migrate
```

Seed sample data:
```bash
python -m scripts.seed
```

This creates 5 authors and 10 books with valid 10-digit ISBNs.

---

### ▶️ Run Locally
Start the server:
```bash
uvicorn app.main:app --reload
```

Visit:
- Swagger Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  
- Health check → [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)  

---

### 🐳 Run with Docker
Build the image:
```bash
docker build -t yipl-backend-2025 .
```

Run the container:
```bash
docker run -p 8000:8000 yipl-backend-2025
```

Now open [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 📚 API Endpoints

### Authors
- **GET /authors** → List authors  
  Query params:
  - `name` (partial match)
  - `sort=book_count`
  - `order=asc|desc` (default: desc)
  - `limit`, `offset`

- **POST /authors** → Create author
```json
{ "name": "Isaac Asimov", "email": "asimov@example.com" }
```

- **GET /authors/{id}** → Single author with their books

---

### Books
- **GET /books** → List books  
  Query params:
  - `title` (partial match)
  - `author` (author name partial match)
  - `year` (published year exact)
  - `sort=title|published_year|created_at`
  - `order=asc|desc`
  - `limit`, `offset`

- **POST /books** → Create book
```json
{ "title": "Foundation", "isbn": "1234567890", "published_year": 1951, "author_id": 1 }
```

- **PUT /books/{id}** → Update book fields  
- **GET /books/{id}** → Single book with author details  

---

### 🔍 Pagination
All list endpoints return:
```json
{
  "data": [...],
  "total": 123,
  "limit": 20,
  "offset": 0
}
```

---

### ❌ Error Responses
**Validation error**
```json
{
  "error": "Validation failed.",
  "details": [
    { "loc": ["body","isbn"], "msg": "ISBN must be exactly 10 digits." }
  ]
}
```

**Not found**
```json
{ "error": "Author not found." }
```

**Conflict**
```json
{ "error": "Email already exists." }
```

---

## 🧪 Running Tests (Optional)
```bash
pytest -q
```

---

