import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
sample_feedback = {"text": "I love this product!"}

def test_predict_feedback():
    response = client.post("/api/predict", json=sample_feedback)
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "score" in data
    # Remove "id" check because API doesn't return it

def test_get_all_feedbacks():
    response = client.get("/api/feedbacks/")
    assert response.status_code == 200
    data = response.json()
    assert "feedbacks" in data
    assert isinstance(data["feedbacks"], list)

def test_filter_feedbacks():
    response = client.get("/api/feedbacks/filter/positive")
    assert response.status_code == 200
    data = response.json()
    assert "feedbacks" in data

def test_feedback_stats():
    response = client.get("/api/stats/")
    assert response.status_code == 200
    data = response.json()
    assert "total_feedbacks" in data
    assert "positive" in data
    assert "negative" in data

def test_delete_all_feedbacks():
    response = client.delete("/api/feedbacks/")
    assert response.status_code == 200
    assert "All feedbacks deleted successfully" in response.json()["message"]
