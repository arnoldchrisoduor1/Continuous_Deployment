import requests
import pytest
import app

BASE = "http://127.0.0.1:5000/"

def test_get_base():
    name = "TestName"       # Example of the name parameter
    test_value = 42         # Example of the integer parameter
    
    # A construct of the full URL with the parameters.
    url = f"{BASE}{name}/{test_value}"
    
    try:
        # Adding a timeout of 5 seconds to the request
        response = requests.get(url, timeout=5)
    except:
        pytest.fail("Request timed out")
        
    # Checking the correct status code.
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    
    # Asserting the returned values.
    json_data = response.json()
    
    # Checking for the correct keys.
    assert "name" in json_data
    assert "test" in json_data
    
    # Checking for the correct data returned
    assert json_data['name'] == name
    assert json_data['test'] == test_value
