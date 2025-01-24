import pytest
from main import app, db
from unittest.mock import MagicMock

@pytest.fixture
def client():
    # Explicitly mock the database and its find method
    mock_items = [{"name": "Test Item", "description": "Test Description", "_id": "mock_id"}]
    db.items.find = MagicMock(return_value=mock_items)
    
    # Create test client
    test_client = app.test_client()
    return test_client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'"status":"200"' in response.data

def test_create_item(client):
    mock_item = {"name":"Test Item", "description":"Test Description"}
    response = client.post('/input', json=mock_item)
    assert response.status_code == 201
    assert b'"name":"Test Item"' in response.data

def test_read_items(client):
    response = client.get('/items')
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data is not None, "Response JSON is empty"
    assert len(data) == 1  
    assert data[0]['name'] == "Test Item"