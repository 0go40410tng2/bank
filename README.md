# Bank Application

## Description
This project is a simple bank application that allows users to create accounts, check balances, and perform transfers. The system uses Python and MySQL to manage user data and perform transactions. It also provides a RESTful API for interacting with the application.

## Installation
To install the necessary dependencies, run the following command:
pip install -r requirements.txt


## Configuration
The application requires the following environment variables:

- `DATABASE_URL`: The connection string to your MySQL database.
- `SECRET_KEY`: A secret key for securing sessions and tokens.

## API Endpoints

| Endpoint        | Method | Description                    |
|-----------------|--------|--------------------------------|
| `/api/users`    | GET    | List all users                 |
| `/api/users`    | POST   | Create a new user              |
| `/api/accounts` | GET    | List all bank accounts         |
| `/api/accounts` | POST   | Create a new bank account      |
| `/api/transfer` | POST   | Transfer funds between accounts|

## Testing
To run the tests, execute the following command:
python test_app.py

Make sure that the database is properly configured before running the tests.

## Git Commit Guidelines
Use conventional commits when making changes to the project. Here are some examples:
```bash
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add user registration tests
