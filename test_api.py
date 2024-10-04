import pytest
from app import app, db

BASE = "http://127.0.0.1:5000/"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            # creating all the tables in the test database
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()
            
def test_register(client):
    # simulating user registrations
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json['msg'] == 'User registered successfully.'
    
def test_login(client):
    # Registering user first before login.
    client.post('/register', json={
        'username': 'testuser',
        'password': 'password'
    })
    
    # Now we can login with the correct credentials.
    response = client.post('/login', json={
        'username': 'testuser',
        'password':'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    
def test_change_password(client):
    # Register and login to get access token
    client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = client.post('/login', json={
        'username':'testuser',
        'password':'testpassword'
    })
    access_token = login_response.json['access_token']
    
    # change password using access token
    response = client.post('/change-password', json={
        'new_password': 'newtestpassword'
    }, headers={
        'Authorization':f'Bearer {access_token}'
    })
    assert response.status_code == 200
    assert response.json['msg'] == 'Password updated successfully.'
    
def test_delete_account(client):
    # Register and login user to get user token.
    client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = client.post('/login', json={
        'username':'testuser',
        'password': 'testpassword'
    })
    access_token = login_response.json['access_token']
    
    # Delete the account using the access token
    response = client.delete('/delete-account', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200
    assert response.json['msg'] == 'Account deleted successfully.'