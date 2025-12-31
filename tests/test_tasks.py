"""Test task endpoints"""
import pytest
from fastapi import status

def test_create_task(client, user_token):
    """Test task creation"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "status": "todo"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["status"] == "todo"
    assert "id" in data

def test_create_task_unauthorized(client):
    """Test task creation without authentication"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_tasks(client, user_token):
    """Test listing tasks"""
    # Create some tasks
    for i in range(5):
        client.post(
            "/api/v1/tasks",
            json={"title": f"Task {i}", "description": f"Description {i}"},
            headers={"Authorization": f"Bearer {user_token}"}
        )
    
    # List tasks
    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["tasks"]) == 5
    assert data["total"] == 5

def test_list_tasks_pagination(client, user_token):
    """Test task pagination"""
    # Create tasks
    for i in range(15):
        client.post(
            "/api/v1/tasks",
            json={"title": f"Task {i}"},
            headers={"Authorization": f"Bearer {user_token}"}
        )
    
    # Get first page
    response = client.get(
        "/api/v1/tasks?skip=0&limit=10",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["tasks"]) == 10
    assert data["total"] == 15
    
    # Get second page
    response = client.get(
        "/api/v1/tasks?skip=10&limit=10",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    data = response.json()
    assert len(data["tasks"]) == 5

def test_list_tasks_filtering(client, user_token):
    """Test task filtering by status"""
    # Create tasks with different statuses
    client.post(
        "/api/v1/tasks",
        json={"title": "Todo Task", "status": "todo"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Done Task", "status": "done"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    # Filter by status
    response = client.get(
        "/api/v1/tasks?status=done",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["status"] == "done"

def test_get_task(client, user_token):
    """Test getting a specific task"""
    # Create task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Get Task Test"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    task_id = create_response.json()["id"]
    
    # Get task
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Get Task Test"

def test_get_nonexistent_task(client, user_token):
    """Test getting a task that doesn't exist"""
    response = client.get(
        "/api/v1/tasks/99999",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_task(client, user_token):
    """Test updating a task"""
    # Create task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original Title"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    task_id = create_response.json()["id"]
    
    # Update task
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated Title", "status": "done"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "done"

def test_partial_update_task(client, user_token):
    """Test partially updating a task"""
    # Create task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original", "description": "Original Desc"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    task_id = create_response.json()["id"]
    
    # Partial update
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": "in_progress"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Original"
    assert data["status"] == "in_progress"

def test_delete_task(client, user_token):
    """Test deleting a task"""
    # Create task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "To Delete"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    task_id = create_response.json()["id"]
    
    # Delete task
    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify deleted
    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_task_access_control(client, user_token):
    """Test that users can't access other users' tasks"""
    # Create second user
    user2_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "user2@example.com",
            "username": "user2",
            "password": "User2Pass123"
        }
    )
    user2_token = user2_response.json()["access_token"]
    
    # User 1 creates task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "User 1 Task"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    task_id = create_response.json()["id"]
    
    # User 2 tries to access
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_admin_access_all_tasks(client, admin_token, user_token):
    """Test that admin can access all tasks"""
    # User creates task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "User Task"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    # Admin gets all tasks
    response = client.get(
        "/api/v1/tasks/admin/all",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
