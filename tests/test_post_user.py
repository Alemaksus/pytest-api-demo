"""User creation tests with validation via JSON Schema and Pydantic."""

import pytest
import allure
from utils.validators import validate_json_schema, validate_pydantic_model, validate_response_time
from utils.helpers import assert_status_code
from utils.models import UserModel
from utils.data_generators import UserDataGenerator

# JSON Schema for validation
user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "role": {"type": "string", "enum": ["user", "admin", "moderator"]}
    },
    "required": ["id", "email", "role"]
}


@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.positive
@allure.title("User creation - successful scenario")
@allure.description("User creation test with response validation via JSON Schema and Pydantic")
def test_create_user_success(auth_client):
    """Test successful user creation with full validation."""
    # Generate test data
    payload = UserDataGenerator.generate_user(role="user")
    
    with allure.step("Sending POST request to create user"):
        resp = auth_client.post("/users", json=payload)
    
    with allure.step("Checking status code"):
        assert_status_code(resp, 201)
    
    with allure.step("Response time validation (should be < 1 sec)"):
        assert validate_response_time(resp, max_time_ms=1000), \
            f"Response time {resp.elapsed.total_seconds() * 1000}ms exceeds 1000ms"
    
    with allure.step("Validation via JSON Schema"):
        body = resp.json()
        validate_json_schema(body, user_schema)
    
    with allure.step("Validation via Pydantic model"):
        user = validate_pydantic_model(body, UserModel)
        assert user.email == payload["email"]
        assert user.role == payload["role"]
    
    with allure.step("Business logic check"):
        assert body["email"] == payload["email"]
        assert body["role"] in ("user", "admin", "moderator")



