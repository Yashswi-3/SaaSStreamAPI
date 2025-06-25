from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_articles_endpoint():
    response = client.get("/articles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
