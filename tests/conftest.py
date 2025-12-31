"""Test configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from app.database import Database
from main import app

@pytest.fixture
def test_db():
    """Create a fresh database for each test"""
    db = Database()
    return db

@pytest.fixture
def client(test_db):
    """Create a test client"""
    # Override the database dependency
    from app import database
    database.db = test_db
    
    client = TestClient(app)
    return client

@pytest.fixture
def admin_token(client):
    """Get admin token for testing"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin123"}
    )
    return response.json()["access_token"]

@pytest.fixture
def user_token(client):
    """Create a test user and get token"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123456"
        }
    )
    return response.json()["access_token"]
