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
    print(json_data)
    assert response.status_code == 201
    assert json_data['message'] == 'Account created successfully'

# Test for retrieving all accounts
def test_get_accounts(client):
    response = client.get('/accounts')
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data, list)  # Should be a list of accounts

# Test for retrieving a single account
def test_get_account(client):
    account_data = {
        'account_id': 7,
        'account_type_code': 5,
        'customer_id': 1,
        'account_name': 'Savings Account',
        'date_opened': '2024-12-15',
        'current_balance': 1000.00,
        'other_account_details': 'Details here'
    }
    client.post('/accounts', json=account_data)  # Creating account first
    response = client.get('/accounts/7')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['account_id'] == 7
    assert json_data['account_name'] == 'Savings Account'

# # Test for updating an account
# def test_update_account(client):
#     account_data = {
#         'account_id': 1,
#         'account_type_code': 101,
#         'customer_id': 1,
#         'account_name': 'Savings Account',
#         'date_opened': '2024-12-15',
#         'current_balance': 1000.00,
#         'other_account_details': 'Details here'
#     }
#     client.post('/accounts', json=account_data)  # Creating account first
#     updated_data = {'account_name': 'Updated Savings Account', 'current_balance': 1200.00}
#     response = client.put('/accounts/1', json=updated_data)
#     json_data = response.get_json()
#     assert response.status_code == 200
#     assert json_data['message'] == 'Account updated successfully'

# # Test for deleting an account
# def test_delete_account(client):
#     account_data = {
#         'account_id': 1,
#         'account_type_code': 101,
#         'customer_id': 1,
#         'account_name': 'Savings Account',
#         'date_opened': '2024-12-15',
#         'current_balance': 1000.00,
#         'other_account_details': 'Details here'
#     }
#     client.post('/accounts', json=account_data)  # Creating account first
#     response = client.delete('/accounts/1')
#     json_data = response.get_json()
#     assert response.status_code == 200
#     assert json_data['message'] == 'Account and related transactions deleted successfully'

# # Test for account not found
# def test_get_account_not_found(client):
#     response = client.get('/accounts/999')
#     json_data = response.get_json()
#     assert response.status_code == 404
#     assert json_data['error'] == 'Account not found'

# # Test for missing required field in account creation
# def test_create_account_missing_field(client):
#     account_data = {
#         'account_id': 1,
#         'account_type_code': 101,
#         'customer_id': 1,
#         'account_name': 'Savings Account',
#         'date_opened': '2024-12-15',
#         'current_balance': 1000.00,
#     }
#     response = client.post('/accounts', json=account_data)
#     json_data = response.get_json()
#     assert response.status_code == 400
#     assert 'Missing field' in json_data['error']

# # Test for database integrity error
# def test_create_account_integrity_error(client):
#     account_data_1 = {
#         'account_id': 1,
#         'account_type_code': 101,
#         'customer_id': 1,
#         'account_name': 'Account 1',
#         'date_opened': '2024-12-15',
#         'current_balance': 1000.00,
#         'other_account_details': 'Details here'
#     }
#     account_data_2 = {
#         'account_id': 1,  # Duplicate account_id which should raise IntegrityError
#         'account_type_code': 101,
#         'customer_id': 1,
#         'account_name': 'Account 2',
#         'date_opened': '2024-12-15',
#         'current_balance': 500.00,
#         'other_account_details': 'Details here'
#     }

#     client.post('/accounts', json=account_data_1)  # First account created
#     response = client.post('/accounts', json=account_data_2)  # Second with duplicate ID
#     json_data = response.get_json()
#     assert response.status_code == 400
#     assert json_data['error'] == 'Database integrity error'