"""
Backend tests for session management (REQ-001)
Following TDD approach - these tests should pass after implementation
"""
import uuid
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_session_returns_201():
    """Test: POST /api/sessions returns 201 and unique session_id"""
    response = client.post("/api/sessions", json={"language": "python"})
    
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data
    assert "created_at" in data
    assert data["language"] == "python"


def test_create_session_generates_valid_uuid():
    """Test: Session ID is valid UUID v4 format"""
    response = client.post("/api/sessions", json={"language": "python"})
    
    assert response.status_code == 201
    data = response.json()
    session_id = data["session_id"]
    
    # Validate it's a valid UUID
    try:
        uuid_obj = uuid.UUID(session_id, version=4)
        assert str(uuid_obj) == session_id
    except ValueError:
        pytest.fail(f"Session ID {session_id} is not a valid UUID v4")


def test_create_session_default_language():
    """Test: Creating session without language defaults to python"""
    response = client.post("/api/sessions", json={})
    
    assert response.status_code == 201
    data = response.json()
    assert data["language"] == "python"


def test_get_session_returns_200():
    """Test: GET /api/sessions/{id} returns 200 with session data"""
    # First create a session
    create_response = client.post("/api/sessions", json={"language": "python"})
    session_id = create_response.json()["session_id"]
    
    # Then retrieve it
    response = client.get(f"/api/sessions/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert data["language"] == "python"
    assert "created_at" in data
    assert "active_users" in data
    assert data["active_users"] == 0


def test_get_nonexistent_session_returns_404():
    """Test: GET non-existent session returns 404"""
    fake_session_id = str(uuid.uuid4())
    response = client.get(f"/api/sessions/{fake_session_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_get_invalid_session_id_returns_404():
    """Test: GET with invalid session ID format returns 404"""
    response = client.get("/api/sessions/not-a-valid-uuid")
    
    assert response.status_code == 404


def test_multiple_concurrent_session_creation():
    """Test: Multiple concurrent session creation works correctly"""
    session_ids = set()
    
    # Create multiple sessions
    for i in range(5):
        response = client.post("/api/sessions", json={"language": "python"})
        assert response.status_code == 201
        session_id = response.json()["session_id"]
        session_ids.add(session_id)
    
    # All session IDs should be unique
    assert len(session_ids) == 5
    
    # All sessions should be retrievable
    for session_id in session_ids:
        response = client.get(f"/api/sessions/{session_id}")
        assert response.status_code == 200
