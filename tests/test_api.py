import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_recommend_products():
    """Test recommendation endpoint"""
    request_data = {
        "query": "red party dress",
    }
    
    response = client.post("/api/v1/recommend", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) <= 3
    assert "processing_time_ms" in data


def test_empty_query():
    """Test with empty query"""
    request_data = {
        "query": "",
        "products": [{"id": 1, "title": "Test", "tags": []}]
    }
    
    response = client.post("/api/v1/recommend", json=request_data)
    assert response.status_code == 400


def test_empty_products():
    """Test with empty products list"""
    request_data = {
        "query": "test",
        "products": []
    }
    
    response = client.post("/api/v1/recommend", json=request_data)
    assert response.status_code == 400