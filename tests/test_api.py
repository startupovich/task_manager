import pytest
from uuid import UUID, uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.database import db
from app.models import Status


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test"""
    db.tasks.clear()
    yield


def test_get_all_tasks_empty():
    """Test getting empty task list"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    """Test task creation with valid data"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == Status.CREATED
    assert UUID(data["id"])


def test_create_task_minimal_data():
    """Test task creation with only required fields"""
    task_data = {"title": "Minimal Task"}
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] is None
    assert data["status"] == Status.CREATED


def test_create_task_invalid_data():
    """Test task creation with invalid data"""
    # Missing required field
    response = client.post("/tasks", json={})
    assert response.status_code == 422
    
    # Empty title
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422
    
    # Title too long (более 200 символов)
    long_title = "a" * 201
    response = client.post("/tasks", json={"title": long_title})
    assert response.status_code == 422
    
    # Description too long (более 1000 символов)
    long_description = "a" * 1001
    response = client.post("/tasks", json={
        "title": "Test", 
        "description": long_description
    })
    assert response.status_code == 422


def test_get_task():
    """Test getting a specific task"""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_nonexistent_task():
    """Test getting a non-existent task"""
    fake_id = uuid4()
    response = client.get(f"/tasks/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_task_invalid_uuid():
    """Test getting a task with invalid UUID format"""
    response = client.get("/tasks/not-a-valid-uuid")
    assert response.status_code == 422


def test_update_task():
    """Test updating a task"""
    # Create a task
    create_response = client.post("/tasks", json={"title": "Original Title"})
    task_id = create_response.json()["id"]
    
    # Update it
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "status": Status.IN_PROGRESS
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["status"] == update_data["status"]


def test_partial_update_task():
    """Test partial task update"""
    # Create a task
    create_response = client.post("/tasks", json={
        "title": "Original Title",
        "description": "Original Description"
    })
    task_id = create_response.json()["id"]
    
    # Update only status
    response = client.put(f"/tasks/{task_id}", json={"status": Status.COMPLETED})
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Original Title"  # Should remain unchanged
    assert data["description"] == "Original Description"  # Should remain unchanged
    assert data["status"] == Status.COMPLETED  # Should be updated


def test_update_nonexistent_task():
    """Test updating a non-existent task"""
    fake_id = uuid4()
    response = client.put(f"/tasks/{fake_id}", json={"title": "New Title"})
    assert response.status_code == 404


def test_delete_task():
    """Test deleting a task"""
    # Create a task
    create_response = client.post("/tasks", json={"title": "To be deleted"})
    task_id = create_response.json()["id"]
    
    # Verify it exists
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    
    # Delete it
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_task():
    """Test deleting a non-existent task"""
    fake_id = uuid4()
    response = client.delete(f"/tasks/{fake_id}")
    assert response.status_code == 404


def test_get_all_tasks_with_data():
    """Test getting all tasks when multiple exist"""
    # Create multiple tasks
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Verify all tasks have required fields
    tasks = response.json()
    for task in tasks:
        assert "id" in task
        assert "title" in task
        assert "status" in task


def test_task_status_validation():
    """Test that only valid status values are accepted"""
    # Create a task
    create_response = client.post("/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]
    
    # Try to set invalid status
    response = client.put(f"/tasks/{task_id}", json={"status": "invalid_status"})
    assert response.status_code == 422