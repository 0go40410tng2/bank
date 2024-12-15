import pytest
from flask import jsonify
from app import create_app, db, Account

@pytest.fixture
def app():
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:bakanese@localhost/test_bank_and_branches',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    # Create the tables in the test database
    with app.app_context():
        db.create_all()
        
    yield app

    # Cleanup the database after tests
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()