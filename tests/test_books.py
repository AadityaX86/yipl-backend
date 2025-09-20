from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test_list_books_filter_by_year():
    r = client.get("/books?year=1937&limit=5")
    assert r.status_code == 200
