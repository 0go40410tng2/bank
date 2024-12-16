import pytest
from flask import jsonify
from app import create_app, db, Account

@pytest.fixture
def app():
    # Create the app instance with the database URI pointing to your existing database
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:bakanese@localhost/test_bank_and_branches',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

 # Set up a database transaction before each test
    with app.app_context():
        db.create_all()
        db.session.begin()  # Begin a transaction

    yield app  # This will run the test

    # After test execution, rollback all changes to the database
    with app.app_context():
        db.session.rollback()  # Rollback any changes
        db.session.remove()  # Remove the session to clean up

@pytest.fixture
def client(app):
    # Return a test client for making HTTP requests
    return app.test_client()

# Test for home route
def test_home(client):
    response = client.get('/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Welcome to the Bank API!'

def test_get_accounts(client):
    # Obtain a valid token by logging in
    login_response = client.post('/login', json={'username': 'admin', 'password': 'admin'})
    
    # Ensure login was successful
    assert login_response.status_code == 200
    
    # Get the token from the response
    token = login_response.get_json()['access_token']  # Access the correct key for the token
    
    # Make authenticated request to the /accounts route
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/accounts', headers=headers)
    
    # Ensure the response is successful
    assert response.status_code == 200

 

# Test for retrieving a single account
def test_get_account(client):
    response = client.get('/accounts/2')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['account_id'] == 2
    assert json_data['account_name'] == 'Acme Savings'

# Test for creating an account
def test_create_account(client):
    account_data = {
        'account_id': 7,
        'account_type_code': 5,
        'customer_id': 1,
        'account_name': 'Savings Account',
        'date_opened': '2024-12-15',
        'current_balance': 1000.00,
        'other_account_details': 'Details here'
    }
    response = client.post('/accounts', json=account_data)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['message'] == 'Account created successfully'

# Test for updating an account
def test_update_account(client):
    updated_data = {'account_name': 'Updated Savings Account', 'current_balance': 1200.00}
    response = client.put('/accounts/7', json=updated_data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Account updated successfully'

# Test for deleting an account
def test_delete_account(client):
    response = client.delete('/accounts/7')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Account and related transactions deleted successfully'

# Test for account not found
def test_get_account_not_found(client):
    response = client.get('/accounts/999')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['error'] == 'Account not found'

# Test for missing required field (e.g. 'account_name')
def test_create_account_missing_field(client):
    account_data = {
        'account_id': 7,
        'account_type_code': 5,
        'customer_id': 1,
        'date_opened': '2024-12-15',
        'current_balance': 1000.00,
        # 'account_name' is missing
    }
    response = client.post('/accounts', json=account_data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert 'Missing field' in json_data['error']


# Test for database integrity error
def test_create_account_integrity_error(client):
    account_data = {
        'account_id': 2,  # Duplicate account_id which should raise IntegrityError
        'account_type_code': 5,
        'customer_id': 1,
        'account_name': 'Account 2',
        'date_opened': '2024-12-15',
        'current_balance': 500.00, 
        'other_account_details': 'Details here'
    }

    response = client.post('/accounts', json=account_data)  # Second with duplicate ID
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['error'] == 'Database integrity error'