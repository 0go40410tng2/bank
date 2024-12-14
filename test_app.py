import pytest
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import patch
from app import app, db, Account

@pytest.fixture
def client():
    # Set up a test client with in-memory database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():  # Ensure the app context is available
        db.create_all()  # Create the database schema
        with app.test_client() as client:
            yield client
        db.drop_all()  # Clean up the database after tests

# Test case for GET /accounts
def test_get_accounts(client):
    # Create an account in the mock database
    account = Account(account_id=1, account_type_code=1, customer_id=1, account_name='Test Account', date_opened='2024-12-14', current_balance=100.00)
    db.session.add(account)
    db.session.commit()

    response = client.get('/accounts')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['account_name'] == 'Test Account'
    assert data[0]['current_balance'] == 100.00

# Test case for GET /accounts/<account_id>
def test_get_account(client):
    account = Account(account_id=1, account_type_code=1, customer_id=1, account_name='Test Account', date_opened='2024-12-14', current_balance=100.00)
    db.session.add(account)
    db.session.commit()

    response = client.get('/accounts/1')
    data = response.get_json()

    assert response.status_code == 200
    assert data['account_name'] == 'Test Account'
    assert data['current_balance'] == 100.00

# Test case for non-existent account
def test_get_account_not_found(client):
    response = client.get('/accounts/9999')
    data = response.get_json()

    assert response.status_code == 404
    assert data['error'] == 'Account not found'

# Test case for POST /accounts
def test_create_account(client):
    new_account_data = {
        'account_id': 2,
        'account_type_code': 1,
        'customer_id': 1,
        'account_name': 'New Account',
        'date_opened': '2024-12-14',
        'current_balance': 200.00
    }

    response = client.post('/accounts', json=new_account_data)
    data = response.get_json()

    assert response.status_code == 201
    assert data['message'] == 'Account created successfully'

# Test case for handling missing fields in POST /accounts
def test_create_account_missing_fields(client):
    new_account_data = {
        'account_id': 2,
        'account_type_code': 1,
        # 'customer_id' is missing
        'account_name': 'New Account',
        'date_opened': '2024-12-14',
        'current_balance': 200.00
    }

    response = client.post('/accounts', json=new_account_data)
    data = response.get_json()

    assert response.status_code == 400
    assert data['error'] == "Missing field: 'customer_id'"

# Test case for PUT /accounts
def test_update_account(client):
    account = Account(account_id=1, account_type_code=1, customer_id=1, account_name='Test Account', date_opened='2024-12-14', current_balance=100.00)
    db.session.add(account)
    db.session.commit()

    updated_data = {
        'account_name': 'Updated Account',
        'current_balance': 150.00
    }

    response = client.put('/accounts/1', json=updated_data)
    data = response.get_json()

    assert response.status_code == 200
    assert data['message'] == 'Account updated successfully'

# Test case for DELETE /accounts
def test_delete_account(client):
    account = Account(account_id=1, account_type_code=1, customer_id=1, account_name='Test Account', date_opened='2024-12-14', current_balance=100.00)
    db.session.add(account)
    db.session.commit()

    response = client.delete('/accounts/1')
    data = response.get_json()

    assert response.status_code == 200
    assert data['message'] == 'Account deleted successfully'

# Test case for DELETE /accounts (non-existent)
def test_delete_account_not_found(client):
    response = client.delete('/accounts/9999')
    data = response.get_json()

    assert response.status_code == 404
    assert data['error'] == 'Account not found'

# Edge Case: Database Integrity Error (e.g., duplicate primary key)
def test_create_account_integrity_error(client):
    account = Account(account_id=1, account_type_code=1, customer_id=1, account_name='Test Account', date_opened='2024-12-14', current_balance=100.00)
    db.session.add(account)
    db.session.commit()

    # Try to create an account with the same ID (violating the primary key constraint)
    new_account_data = {
        'account_id': 1,  # Duplicate account_id
        'account_type_code': 1,
        'customer_id': 1,
        'account_name': 'Duplicate Account',
        'date_opened': '2024-12-14',
        'current_balance': 150.00
    }

    response = client.post('/accounts', json=new_account_data)
    data = response.get_json()

    assert response.status_code == 400
    assert data['error'] == 'Database integrity error'
