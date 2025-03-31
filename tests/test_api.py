import pytest
from app import app, db, Task

@pytest.fixture
def client():
    """Create a Flask test client with a fresh database."""
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client  # Provide the test client
        with app.app_context():
            db.drop_all()  # Cleanup after tests

def test_create_task(client):
    """Test creating a new task."""
    response = client.post("/tasks", json={"title": "Test Task", "description": "This is a test."})
    assert response.status_code == 201
    assert response.json["message"] == "Task created"

def test_get_tasks(client):
    """Test retrieving all tasks."""
    client.post("/tasks", json={"title": "Task 1", "description": "Desc 1"})
    client.post("/tasks", json={"title": "Task 2", "description": "Desc 2"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json) == 2  # Two tasks should exist

def test_get_task_by_id(client):
    """Test retrieving a specific task by ID."""
    client.post("/tasks", json={"title": "Task 1", "description": "Desc 1"})
    
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json["title"] == "Task 1"

def test_update_task(client):
    """Test updating an existing task."""
    client.post("/tasks", json={"title": "Old Task", "description": "Old Desc"})
    
    response = client.put("/tasks/1", json={"title": "Updated Task"})
    assert response.status_code == 200
    assert response.json["message"] == "Task updated successfully"

    response = client.get("/tasks/1")
    assert response.json["title"] == "Updated Task"

def test_delete_task(client):
    """Test deleting a task."""
    client.post("/tasks", json={"title": "Task to Delete"})
    
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json["message"] == "Task deleted successfully"

    response = client.get("/tasks/1")
    assert response.status_code == 404  # Task should be gone
