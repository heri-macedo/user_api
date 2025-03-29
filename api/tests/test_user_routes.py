import pytest


class TestGetUserRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, app, user, client):
        self.user = user
        self.client = client


    def test_list_users_success(self):
        response = self.client.get('/users/')
        assert response.status_code == 200

        data = response.get_json()
        users_list = data.get("users")
        assert isinstance(users_list, list)
        assert len(users_list) == 1


    def test_list_users_invalid_page(self):
        invalid_page = 0
        response = self.client.get(f"/users/?page={invalid_page}")
        assert response.status_code == 422
        assert response.get_json()["errors"][0] == "Input should be greater than or equal to 1"


    def test_list_users_invalid_per_page_min_value(self):
        invalid_per_page = 0
        response = self.client.get(f"/users/?per_page={invalid_per_page}")
        assert response.status_code == 422
        assert response.get_json()["errors"][0] == "Input should be greater than or equal to 1"


    def test_list_users_invalid_per_page_max_value(self):
        invalid_per_page = 1000
        response = self.client.get(f"/users/?per_page={invalid_per_page}")
        assert response.status_code == 422
        assert response.get_json()["errors"][0] == "Input should be less than 100"


    def test_get_user_by_id_success(self):
        user_id = self.user["id"]
        response = self.client.get(f"/users/{user_id}")
        assert response.status_code == 200

        data = response.get_json()

        assert data["email"] == self.user["email"]
        assert data["username"] == self.user["username"]
        assert data["id"] == user_id

    def test_get_user_by_id_invalid(self):
        user_id = 50
        response = self.client.get(f"/users/{user_id}")
        assert response.status_code == 404

        assert response.get_json()["errors"] == "User does not exist"

class TestCreateUserRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, app, client, user):
        self.client = client
        self.user = user
    
    def test_create_user_success(self):
        payload = {
            "username": "foo_bar_doe",
            "email": "foo_bar_doe@example.com",
            "password": "secret123"
        }
        response = self.client.post('/users/', json=payload)
        assert response.status_code == 201


    def test_create_user_invalid_email(self):
        payload = {
            "username": "foo_bar_doe",
            "email": "foo_bar_doe-example.com",
            "password": "secret123"
        }
        response = self.client.post('/users/', json=payload)
        assert response.status_code == 422


    def test_create_user_invalid_username(self):
        payload = {
            "username": "foo",
            "email": "foo_bar_doe@example.com",
            "password": "secret123"
        }
        response = self.client.post('/users/', json=payload)
        assert response.status_code == 422
        assert response.get_json()["errors"][0] == "String should have at least 8 characters"


    def test_create_user_invalid_password(self):
        payload = {
            "username": "foo",
            "email": "foo_bar_doe@example.com",
            "password": "12345678"
        }
        response = self.client.post('/users/', json=payload)

        assert response.status_code == 422
        assert response.get_json()["errors"][0] == "String should have at least 8 characters"


    def test_create_user_invalid_password_and_username(self):
        payload = {
            "username": "foo",
            "email": "foo_bar_doe@example.com",
            "password": "1234"
        }
        response = self.client.post('/users/', json=payload)

        assert response.status_code == 422
        assert set(response.get_json()["errors"]) == set(["String should have at least 8 characters"])

    def test_create_existing_email(self):
        payload = {
            "username": "foo_bar_doe",
            "email": self.user["email"],
            "password": "teste12345"
        }
        response = self.client.post('/users/', json=payload)
        assert response.status_code == 400
        assert response.get_json()["errors"] == "Email already in use"

    def test_create_existing_username(self):
        payload = {
            "username": self.user["username"],
            "email": "new_email_test@gmail.com",
            "password": "teste12345"
        }
        response = self.client.post('/users/', json=payload)
        assert response.status_code == 400
        assert response.get_json()["errors"] == "Username already in use"

class TestUpdateUserRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, app, client, user):
        self.client = client
        self.user = user

    def test_update_username_success(self):
        user = self.user
        payload = {
            "username": "new_username",
        }
        request = self.client.put(f"/users/{user['id']}", json=payload)
        assert request.status_code == 201
        assert request.get_json()["message"] == f"User {user["id"]} updated"

    def test_update_username_invalid(self):
        user = self.user
        payload = {
            "username": "foo",
        }
        request = self.client.put(f"/users/{user["id"]}", json=payload)
        assert request.status_code == 422
        assert request.get_json()["errors"][0] == "String should have at least 8 characters"

    def test_update_existing_username(self):
        user = self.user
        payload = {
            "username": self.user["username"],
        }
        request = self.client.put(f"/users/{user["id"]}", json=payload)
        assert request.status_code == 400
        assert request.get_json()["errors"] == "Username matches current one"
    
    def test_update_existing_email(self):
        user = self.user
        payload = {
            "email": self.user["email"],
        }
        request = self.client.put(f"/users/{user["id"]}", json=payload)
        assert request.status_code == 400
        assert request.get_json()["errors"] == "Email matches current one"

class TestDeleteUserRoutes:
    @pytest.fixture(autouse=True)
    def setup(self, app, client, user):
        self.client = client
        self.user = user

    def test_delete_user_success(self):
        user = self.user
        response = self.client.delete(f"/users/{user["id"]}")
        assert response.status_code == 200
        assert response.get_json()["message"] == "User deleted successfully"

    def test_delete_user_invalid(self):
        user_id_invalid = 50
        response = self.client.delete(f"/users/{user_id_invalid}")
        assert response.status_code == 400
        assert response.get_json()["errors"] == "User does not exist"

    def test_wrong_body_params(self):
        user = self.user
        payload = {
            "username": "new_username",
        }
        response = self.client.delete(f"/users/{user["id"]}", json=payload)
        assert response.status_code == 400
        assert response.get_json()["errors"] == "Endpoint dos not expect body params"