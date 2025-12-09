"""
Integration tests for FastAPI backend endpoints.

Tests the interaction between client and server for existing endpoints.
"""

import pytest
from fastapi import status


class TestHealthEndpoint:
    """Test suite for health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Test that health endpoint returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK

    def test_health_check_returns_correct_json(self, client):
        """Test that health endpoint returns correct JSON structure."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "ok"

    def test_health_check_content_type(self, client):
        """Test that health endpoint returns JSON content type."""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]


class TestRootEndpoint:
    """Test suite for root endpoint."""

    def test_root_returns_200(self, client):
        """Test that root endpoint returns 200 OK."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK

    def test_root_returns_api_information(self, client):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data
        
        assert data["name"] == "Collaborative Coding Interview Platform API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"

    def test_root_content_type(self, client):
        """Test that root endpoint returns JSON content type."""
        response = client.get("/")
        assert "application/json" in response.headers["content-type"]


class TestCORS:
    """Test suite for CORS configuration."""

    def test_cors_allows_localhost_5173(self, client):
        """Test that CORS allows localhost:5173 origin."""
        headers = {"Origin": "http://localhost:5173"}
        response = client.get("/health", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:5173"

    def test_cors_allows_localhost_3000(self, client):
        """Test that CORS allows localhost:3000 origin."""
        headers = {"Origin": "http://localhost:3000"}
        response = client.get("/health", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestAPIDocumentation:
    """Test suite for API documentation endpoints."""

    def test_openapi_json_accessible(self, client):
        """Test that OpenAPI JSON schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    def test_swagger_docs_accessible(self, client):
        """Test that Swagger UI docs are accessible."""
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK

    def test_redoc_docs_accessible(self, client):
        """Test that ReDoc docs are accessible."""
        response = client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK


class TestErrorHandling:
    """Test suite for error handling."""

    def test_404_for_nonexistent_route(self, client):
        """Test that nonexistent routes return 404."""
        response = client.get("/nonexistent-route")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_405_for_wrong_method(self, client):
        """Test that wrong HTTP methods return 405."""
        response = client.post("/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
