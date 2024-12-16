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

# API Endpoints

| HTTP Method | Endpoint                  | Description                                                    | Requirements                    |
|-------------|---------------------------|----------------------------------------------------------------|---------------------------------|
| **GET**     | `/`                       | Returns a welcome message and a list of available endpoints.  | None                            |
| **POST**    | `/login`                  | Authenticates a user and returns a JWT token if valid.         | None                            |
| **GET**     | `/accounts`               | Retrieves a list of all accounts.                              | JWT required, "admin" role      |
| **GET**     | `/accounts/<int:account_id>` | Retrieves details of a specific account by ID.               | JWT required, "admin" role      |
| **POST**    | `/accounts`               | Creates a new account.                                         | None explicitly mentioned       |
| **PUT**     | `/accounts/<int:account_id>` | Updates details of a specific account by ID.                 | None explicitly mentioned       |
| **DELETE**  | `/accounts/<int:account_id>` | Deletes an account and its related transaction messages.      | None explicitly mentioned       |


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
