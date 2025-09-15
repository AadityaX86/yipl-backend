from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import time

from app.routers import authors as authors_router
from app.routers import books as books_router

#app
app = FastAPI(
    title="Library Management API",
    version="1.0.0",
    description="RESTful API for managing authors and books (YIPL Internship Task).",
)

#  Logging 
logger = logging.getLogger("app")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %s (%.1f ms)",
                request.method, request.url.path, response.status_code, duration_ms)
    return response

# Unified Error Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exc_handler(_: Request, exc: StarletteHTTPException):
    # Ensures errors raised via fastapi.HTTPException become {"error": "..."}
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exc_handler(_: Request, exc: RequestValidationError):
    details = [{"loc": e.get("loc"), "msg": e.get("msg")} for e in exc.errors()]
    return JSONResponse(status_code=400, content={"error": "Validation failed.", "details": details})

# Health
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Routers
app.include_router(authors_router.router)
app.include_router(books_router.router)
