import pytest
import app

@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client

def test_get_base(client):
    name = "arnold"  # Example name parameter
    test_value = 19   # Example integer test parameter

    # Send a GET request with parameters
    response = client.get(f"/{name}/{test_value}")
    
    # Check the status code
    assert response.status_code == 200
    
    # Get the JSON response
    json_data = response.get_json()
    
    # Assert the returned values
    assert json_data["name"] == name
    assert json_data["test"] == test_value