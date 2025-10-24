from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_sentiment_positive():
    response = client.post("/analyze", json={"text": "I love programming!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment_result"]["label"] == "positive"


def test_sentiment_negative():
    response = client.post("/analyze", json={"text": "I hate bugs."})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment_result"]["label"] == "negative"
