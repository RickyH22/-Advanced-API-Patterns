"""Test middleware and error handling"""
import pytest
from fastapi import status

def test_request_id_header(client):
    """Test that request ID is added to responses"""
    response = client.get("/")
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0

def test_process_time_header(client):
    """Test that process time is added to responses"""
    response = client.get("/")
    assert "X-Process-Time" in response.headers

def test_cors_headers(client):
    """Test CORS headers are present"""
    response = client.options("/")
    assert "access-control-allow-origin" in response.headers

def test_error_response_format(client):
    """Test standardized error response format"""
    response = client.get(
        "/api/v1/tasks/99999",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]
    assert "request_id" in data["error"]

def test_validation_error(client, user_token):
    """Test validation error handling"""
    response = client.post(
        "/api/v1/tasks",
        json={"title": ""},  # Empty title should fail validation
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
