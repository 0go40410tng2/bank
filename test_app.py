import pytest
from app import app, db, Account

@pytest.fixture
def client():
    # Configure app for testing
    app.config.from_object('test_config')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
        yield client
        # Teardown
        with app.app_context():
            db.session.remove()
            db.drop_all()

@pytest.fixture
def mock_account_data():
    """Provide mock data for accounts."""
    return [
        Account(account_id=1, account_type_code=101, customer_id=1, account_name="Test Account 1", 
                date_opened="2024-12-01", current_balance=1000.00),
        Account(account_id=2, account_type_code=102, customer_id=2, account_name="Test Account 2", 
                date_opened="2024-12-02", current_balance=2000.00)
    ]