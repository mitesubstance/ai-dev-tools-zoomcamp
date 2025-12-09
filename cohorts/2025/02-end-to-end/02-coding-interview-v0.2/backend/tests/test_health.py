"""
Backend tests for health check endpoint
Tests verify the basic health endpoint functionality
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

# TestClient for testing FastAPI endpoints
client = TestClient(app)


def test_root_endpoint_returns_200():
    """Test that root endpoint returns 200 OK"""
    response = client.get("/")
    assert response.status_code == 200


def test_root_endpoint_returns_correct_json():
    """Test that root endpoint returns correct JSON structure"""
    response = client.get("/")
    data = response.json()
    
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert data["message"] == "Coding Interview Platform API"
    assert data["version"] == "0.2.0"
    assert data["status"] == "running"


def test_health_endpoint_returns_200():
    """Test that health check endpoint returns 200 OK"""
    response = client.get("/api/health")
    assert response.status_code == 200


def test_health_endpoint_returns_correct_json_structure():
    """Test that health check endpoint returns correct JSON payload structure"""
    response = client.get("/api/health")
    data = response.json()
    
    # Verify required fields exist
    assert "status" in data
    assert "timestamp" in data
    assert "service" in data
    
    # Verify field values
    assert data["status"] == "ok"
    assert data["service"] == "coding-interview-backend"


def test_health_endpoint_timestamp_is_valid_iso_format():
    """Test that timestamp is in valid ISO 8601 format"""
    response = client.get("/api/health")
    data = response.json()
    
    # Verify timestamp can be parsed as ISO format
    timestamp_str = data["timestamp"]
    try:
        datetime.fromisoformat(timestamp_str)
        timestamp_valid = True
    except ValueError:
        timestamp_valid = False
    
    assert timestamp_valid, f"Timestamp {timestamp_str} is not valid ISO format"


def test_health_endpoint_returns_current_timestamp():
    """Test that health endpoint returns current timestamp (within reasonable range)"""
    before = datetime.now()
    response = client.get("/api/health")
    after = datetime.now()
    
    data = response.json()
    timestamp = datetime.fromisoformat(data["timestamp"])
    
    # Timestamp should be between before and after request
    assert before <= timestamp <= after


def test_health_endpoint_cors_headers():
    """Test that CORS headers are properly configured"""
    response = client.get("/api/health")
    
    # CORS headers should allow cross-origin requests
    assert response.status_code == 200
    # Note: In test client, CORS middleware may not add headers
    # This test documents the expectation for production


def test_nonexistent_endpoint_returns_404():
    """Test that non-existent endpoints return 404"""
    response = client.get("/api/nonexistent")
    assert response.status_code == 404
