"""Test authentication endpoints"""
import pytest
from fastapi import status

def test_register_success(client):
    """Test successful user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "NewUser123"
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "newuser@example.com"

def test_register_duplicate_username(client, user_token):
    """Test registration with duplicate username"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "another@example.com",
            "username": "testuser",
            "password": "Test123456"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["error"]["message"].lower()

def test_register_weak_password(client):
    """Test registration with weak password"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "weak@example.com",
            "username": "weakpass",
            "password": "weak"
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_login_success(client, user_token):
    """Test successful login"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "Test123456"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "testuser"

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "nonexistent",
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_password_validation(client):
    """Test password validation rules"""
    # No uppercase
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test1@example.com",
            "username": "test1",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # No digit
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test2@example.com",
            "username": "test2",
            "password": "Password"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
