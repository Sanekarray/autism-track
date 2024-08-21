import pytest
from app import app, patient_ids, users  # Import the Flask app and necessary variables

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test if the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Autism Track" in response.data  # Ensure this matches the content of your index.html

def test_autism_page(client):
    """Test if the autism page loads successfully."""
    response = client.get('/autism')
    assert response.status_code == 200
    assert b"Autism" in response.data  # Ensure this matches the content of your autism.html

def test_login_page_loads(client):
    """Test if the login page loads successfully."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login to Autism Track" in response.data  # Ensure this matches the content of your login.html


def test_invalid_login(client):
    """Test if the login fails with incorrect credentials."""
    response = client.post('/login', data=dict(
        email='user@example.com',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid credentials. Please try again." in response.data  # Ensure this matches the flash message in your login view

def test_login_with_missing_fields(client):
    """Test if the login fails when fields are missing."""
    response = client.post('/login', data=dict(
        email='user@example.com',
        password=''
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Please provide both email and password." in response.data  # Ensure this matches the flash message in your login view

