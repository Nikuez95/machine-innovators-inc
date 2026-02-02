# Ho scritto dei test di base per verificare che l'API funzioni correttamente.

# Importo le librerie necessarie
from fastapi.testclient import TestClient
from app.main import app

# Creo il client di test
client = TestClient(app)


# Test per la route principale
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


# Test per l'analisi del sentiment positivo
def test_sentiment_positive():
    response = client.post("/analyze", json={"text": "I love programming!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"]["label"] == "positive"


# Test per l'analisi del sentiment negativo
def test_sentiment_negative():
    response = client.post("/analyze", json={"text": "I hate bugs."})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"]["label"] == "negative"


# Test per l'analisi del sentiment neutro
def test_sentiment_neutral():
    response = client.post("/analyze", json={"text": "I'm here."})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"]["label"] == "neutral"
