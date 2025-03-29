# User API

This API provides endpoints for managing users. It supports listing, retrieving, creating, updating, and deleting user records. The API uses Flask as the web framework, SQLAlchemy for ORM, and Pydantic for input validation.

---

## Local Setup

### 1. Clone the Repository

```
git clone https://github.com/heri-macedo/user_api.git
```

cd user_api

### 2. Create and Activate a Virtual Environment

Create a virtual environment using Python's venv module:

```
python -m venv venv
```

Activate the virtual environment:

On Linux/macOS:

```
source venv/bin/activate
```

### 3. Install Dependencies

After activating your virtual environment, install the required packages:

```
pip install -r requirements.txt
```

### 4. Environment Variables

Ensure that you have a .flaskenv file in the root directory with the following content:

```
FLASK_APP=api:create_app
FLASK_DEBUG=1
```

This file allows Flask to load the correct application factory and enable debug mode automatically.

### 5. Using the Makefile

The repository includes a Makefile with useful commands:

- Run Tests Local
  Run tests locally on venv
  Command: ```make run-tests-local```

- Run Tests :
  Rebuilds the test image (ignoring cache) and executes the tests in the Docker container.
  Command: ```make run-tests```

- Run Development Environment:
  Starts the development environment via Docker. This environment mounts your source code so that changes are reflected instantly.
  Command: ```make run-dev```

- Run Flask Locally:
  Starts the Flask server locally (outside Docker) on port 5000.
  Command: ```make run-flask```

---

## API Endpoints

The following table describes each API route, including its HTTP method, URL, expected parameters, request body (if applicable), and the typical response.

| **Method** | **URL**                   | **Parameters / Query String**                                | **Request Body**                                                                                                                                                        | **Response**                                                                                                                                                                |
|------------|---------------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET        | `/users/`                 | Query: `page` (int, optional), `per_page` (int, optional)      | None. Note: The endpoint does not accept a body. If a body is sent, a 400 error is returned.                                                                             | Returns a JSON object with pagination metadata and a list of users. Example: `{ "users": [...], "total": X, "page": 1, "pages": Y, "next_page": Z, "per_page": 10 }`      |
| GET        | `/users/<int:id>`         | URL parameter: `id` (int)                                      | None. Note: The endpoint does not accept a body.                                                                                                                      | Returns the user record as JSON if found (status 200) or an error message (e.g., "User does not exist") with a 404 status.                                                 |
| POST       | `/users/`                 | None                                                         | JSON payload with keys: `username`: string, `email`: string (validated via Pydantic), `password`: string                                                                 | Returns a JSON object confirming successful creation with a message (or optionally the user data) and status 201.                                                          |
| PUT        | `/users/<int:id>`         | URL parameter: `id` (int)                                      | JSON payload with fields to update (all optional): `username`: string, `email`: string, `password`: string (only fields provided will be updated)                   | Returns a JSON object with a message indicating success (e.g., "User <id> updated") and status 201, or a validation/business error with the appropriate status code.    |
| DELETE     | `/users/<int:id>`         | URL parameter: `id` (int)                                      | No body is expected. If a body is provided, a 400 error is returned.                                                                                                    | Returns a JSON object with a message confirming deletion (e.g., "User deleted successfully") and status 200 (or 204 if preferred).                                           |

**Error Handling:**
- **Validation Errors:** When data fails Pydantic validation (e.g., invalid email format or missing fields), the API returns a 422 status with an "errors" array containing the validation messages.
- **Value Errors / Business Logic Errors:** If a user already exists, or a field is unchanged (like email or username), the API returns a 400 status with an appropriate error message.
- **Unexpected Errors:** For any other exceptions, the API returns a 500 status with a generic error message.


---

## Running the Application

Locally (outside Docker):
Make sure to activate your virtual environment and ensure your .flaskenv file is in place. Then run:
```
make run-flask
```

In Docker (Development Environment):
Use:
```
make run-dev
```

Running Tests:
To run the test suite in a Docker container:
```
make run-tests
```
