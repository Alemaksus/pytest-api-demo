"""CRUD tests for users using fixtures and utilities."""

import pytest
import allure
from utils.helpers import assert_status_code, extract_json_field
from utils.validators import validate_response_time
from utils.data_generators import UserDataGenerator
from utils.models import UserModel
from utils.validators import validate_pydantic_model


@pytest.mark.crud
@pytest.mark.api
@pytest.mark.regression
@allure.title("Full user CRUD cycle")
@allure.description("Test for creating, reading, updating, and deleting a user")
def test_crud_user(auth_client, clean_user_data):
    """Test full CRUD operations cycle for a user."""
    
    # ---------- CREATE ----------
    with allure.step("Creating new user"):
        payload = UserDataGenerator.generate_user()
        response = auth_client.post("/users", json=payload)
        assert_status_code(response, 201)
        
        # Response time validation
        assert validate_response_time(response, max_time_ms=1000), \
            "Create operation took too long"
        
        user_id = extract_json_field(response, "id")
        clean_user_data.append(user_id)  # For cleanup
        
        # Validation via Pydantic
        user = validate_pydantic_model(response.json(), UserModel)
        assert user.email == payload["email"]

    # ---------- READ ----------
    with allure.step("Reading created user"):
        response = auth_client.get(f"/users/{user_id}")
        assert_status_code(response, 200)
        
        assert validate_response_time(response, max_time_ms=500), \
            "Read operation took too long"
        
        user_data = response.json()
        assert user_data["email"] == payload["email"]
        assert user_data["name"] == payload["name"]

    # ---------- UPDATE ----------
    with allure.step("Updating user data"):
        updated = {
            "name": "Aleksandr",
            "surname": "Updated",
            "email": payload["email"]
        }
        response = auth_client.put(f"/users/{user_id}", json=updated)
        assert_status_code(response, 200)
        
        # Verify that data was updated
        updated_user = response.json()
        assert updated_user["name"] == updated["name"]

    # ---------- DELETE ----------
    with allure.step("Deleting user"):
        response = auth_client.delete(f"/users/{user_id}")
        assert_status_code(response, 204)

    # ---------- READ AFTER DELETE ----------
    with allure.step("Verifying user is deleted"):
        response = auth_client.get(f"/users/{user_id}")
        assert_status_code(response, 404)
        
        # Remove from list since already deleted
        clean_user_data.remove(user_id)
