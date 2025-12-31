"""Test health and async endpoints"""
import pytest
from fastapi import status

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check(client):
    """Test basic health check"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_detailed_health_check(client):
    """Test detailed health check"""
    response = client.get("/health/detailed")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "status" in data
    assert "dependencies" in data
    assert "database" in data["dependencies"]

def test_async_external_endpoint(client):
    """Test async external API call"""
    response = client.get("/async/external")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Either successfully fetched data or got an error message
    assert "source" in data or "error" in data

def test_background_task_endpoint(client):
    """Test background task triggering"""
    response = client.post("/async/background-task?task_name=test_task")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Background task triggered"
    assert data["task_name"] == "test_task"
