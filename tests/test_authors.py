from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test_create_author_success():
    r = client.post("/authors", json={"name":"Isaac Asimov","email":"asimov@example.com"})
    assert r.status_code == 201
def test_create_author_invalid_email():
    r = client.post("/authors", json={"name":"Bad","email":"not-an-email"})
    assert r.status_code == 400
