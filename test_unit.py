import pytest
from app import app, db
from models import User

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite DB for testing
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Set up database tables for each test
        yield client
        with app.app_context():
            db.drop_all()  # Teardown database after each test

def test_register(test_client):
    response = test_client.post('/register', json={
        'username': 'arnold',
        'password': 'password123'
    })
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['msg'] == 'User registered successfully.'

def test_login(test_client):
    # First, register a user
    test_client.post('/register', json={
        'username': 'arnold',
        'password': 'password123'
    })

    # Then login with correct credentials
    response = test_client.post('/login', json={
        'username': 'arnold',
        'password': 'password123'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'access_token' in json_data

def test_change_password(test_client):
    # Register and login to get access token
    test_client.post('/register', json={
        'username': 'arnold',
        'password': 'password123'
    })
    login_response = test_client.post('/login', json={
        'username': 'arnold',
        'password': 'password123'
    })
    access_token = login_response.get_json()['access_token']

    # Change password using the access token
    response = test_client.post('/change-password', json={
        'new_password': 'newpassword123'
    }, headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['msg'] == 'Password updated successfully.'

def test_delete_account(test_client):
    # Register and login to get access token
    test_client.post('/register', json={
        'username': 'arnold',
        'password': 'password123'
    })
    login_response = test_client.post('/login', json={
        'username': 'arnold',
        'password': 'password123'
    })
    access_token = login_response.get_json()['access_token']

    # Delete the account using the access token
    response = test_client.delete('/delete-account', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['msg'] == 'Account deleted successfully.'
