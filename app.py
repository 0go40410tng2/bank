from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:bakanese@localhost/bank_and_branches'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config:
        app.config.update(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    register_error_handlers(app)

    return app

# Register routes
def register_routes(app):
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Welcome to the Bank API!',
            'endpoints': {
                '/accounts': 'Manage accounts',
                '/accounts/<account_id>': 'Manage a specific account'
            }
        })

    @app.route('/accounts', methods=['GET'])
    def get_accounts():
        accounts = Account.query.all()
        return jsonify([{
            'account_id': a.account_id,
            'account_name': a.account_name,
            'current_balance': float(a.current_balance)
        } for a in accounts])

    @app.route('/accounts/<int:account_id>', methods=['GET'])
    def get_account(account_id):
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        return jsonify({
            'account_id': account.account_id,
            'account_name': account.account_name,
            'current_balance': float(account.current_balance)
        })

    @app.route('/accounts', methods=['POST'])
    def create_account():
        data = request.get_json()
        try:
            new_account = Account(
                account_id=data['account_id'],
                account_type_code=data['account_type_code'],
                customer_id=data['customer_id'],
                account_name=data['account_name'],
                date_opened=data['date_opened'],
                current_balance=data['current_balance'],
                other_account_details=data.get('other_account_details')
            )
            db.session.add(new_account)
            db.session.commit()
            return jsonify({'message': 'Account created successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Database integrity error'}), 400
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e}'}), 400

    @app.route('/accounts/<int:account_id>', methods=['PUT'])
    def update_account(account_id):
        data = request.get_json()
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404

        account.account_name = data.get('account_name', account.account_name)
        account.current_balance = data.get('current_balance', account.current_balance)
        account.other_account_details = data.get('other_account_details', account.other_account_details)

        db.session.commit()
        return jsonify({'message': 'Account updated successfully'})

    @app.route('/accounts/<int:account_id>', methods=['DELETE'])
    def delete_account(account_id):
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404

        # Delete related transaction messages
        TransactionMessage.query.filter_by(account_id=account_id).delete()

        # Now delete the account
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Account and related transactions deleted successfully'})

# Register error handlers
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500

# Models
class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_type_code = db.Column(db.Integer, db.ForeignKey('ref_customer_types.customer_type_code'))
    customer_name = db.Column(db.String(255))
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(255))
    date_became_customer = db.Column(db.Date)
    other_details = db.Column(db.Text)

class Account(db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    account_type_code = db.Column(db.Integer, db.ForeignKey('ref_account_types.account_type_code'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    account_name = db.Column(db.String(255))
    date_opened = db.Column(db.Date)
    date_closed = db.Column(db.Date, nullable=True)
    current_balance = db.Column(db.Numeric(18, 2))
    other_account_details = db.Column(db.Text)

class RefAccountType(db.Model):
    __tablename__ = 'ref_account_types'
    account_type_code = db.Column(db.Integer, primary_key=True)
    account_type_description = db.Column(db.String(255))

class RefCustomerType(db.Model):
    __tablename__ = 'ref_customer_types'
    customer_type_code = db.Column(db.Integer, primary_key=True)
    customer_type_description = db.Column(db.String(255))

class Party(db.Model):
    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    other_details = db.Column(db.Text, nullable=True)

class TransactionMessage(db.Model):
    __tablename__ = 'transaction_messages'  # Ensure this matches the table name in your database
    __table_args__ = {'extend_existing': True}

    message_number = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'))
    counterparty_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'))
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'))
    transaction_type_code = db.Column(db.Integer, db.ForeignKey('ref_transaction_types.transaction_type_code'))
    counterparty_role = db.Column(db.String(255), nullable=True)
    currency_code = db.Column(db.String(10), nullable=True)
    iban_number = db.Column(db.String(34), nullable=True)
    transaction_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Numeric(18, 2), nullable=True)
    balance = db.Column(db.Numeric(18, 2), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    party_role = db.Column(db.String(255), nullable=True)

    # Define the relationships
    account = db.relationship('Account', backref='transactions', lazy=True)
    counterparty = db.relationship('Party', foreign_keys=[counterparty_id])
    party = db.relationship('Party', foreign_keys=[party_id])
    transaction_type = db.relationship('RefTransactionType', backref='transaction_messages', lazy=True)

class RefTransactionType(db.Model):
    __tablename__ = 'ref_transaction_types'

    transaction_type_code = db.Column(db.Integer, primary_key=True)
    transaction_type_description = db.Column(db.String(255), nullable=True)


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
