import pytest
from main import app
from unittest.mock import MagicMock
import os
os.environ["TEST_ENV"] = "true"
@pytest.fixture
def client():
    app.config['TEST_ENV'] = 'true'  # Use mock database for testing
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'"status":"200"' in response.data

def test_create_item(client):
    # Prepare mock data
    mock_item = {"name":"Test Item", "description":"Test Description"}
    
    # Mock the insert_one method
    mock_db = MagicMock()
    app.db = mock_db
    app.db.items.insert_one.return_value = True  # Mock insert_success
    
    # Make POST request to create an item
    response = client.post('/input', json=mock_item)
    assert response.status_code == 201
    assert b'"message":"Item created successfully"' in response.data
    assert b'"name":"Test Item"' in response.data

# def test_read_items(client):
#     # Mock the items in the database
#     mock_db = MagicMock()
#     app.db = mock_db
#     mock_items = {"name":"Test Item", "description":"Test Description"}

#     client.post('/input', json=mock_items)

#     items = list(app.db.items.find())  # Ensure the cursor is fully consumed into a list
#     for item in items:
#         item['_id'] = str(item['_id'])  # Convert ObjectId to string for JSON compatibility - needed in order to pull the data
#     # return jsonify(items)

#     # app.db.items.find.return_value = mock_items
#     # Make GET request to fetch all items
#     response = client.get('/items')
#     print(f"Response status code: {response.status_code}")
#     print(f"Response data: {response.data}")
#     assert response.status_code == 200
#     assert len(response.json) == 1  # Check that 1 item was returned
#     assert response.json[0]['name'] == "Test Item"  # Check that the item is correct



def test_read_items(client):
    # Mock the items in the database
    app.db = MagicMock()
    

    # Prepare mock data for items
    mock_items = [{"name": "Test Item", "description": "Test Description"}]

    # Mock the cursor returned by db.items.find
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter(mock_items)  # Simulate cursor iteration
    
    # Set the mock to return the cursor-like object when find is called
    app.db.items.find.return_value = mock_cursor

    # Make GET request to fetch all items
    response = client.get('/items')
    
    # Debug: Print the full response to understand what's returned
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")

    # Assert response status code
    assert response.status_code == 200
    
    # Check if the number of items returned is 1
    assert len(response.json) == 1  # Expecting 1 item in the response
    assert response.json[0]['name'] == "Test Item"  # Check the name of the first item
