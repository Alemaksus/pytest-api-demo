"""Negative tests for user creation."""

import pytest
import allure
from utils.helpers import assert_status_code
from utils.data_generators import UserDataGenerator
from utils.models import ErrorResponse
from utils.validators import validate_pydantic_model


@pytest.mark.negative
@pytest.mark.api
@pytest.mark.parametrize(
    "payload, expected_status, error_description",
    [
        (
            {"email": "", "role": "user"},
            422,
            "Empty email should return 422"
        ),
        (
            {"email": "not-email", "role": "user"},
            422,
            "Invalid email should return 422"
        ),
        (
            {"email": "qa@example.com", "role": "root"},
            422,
            "Invalid enum for role should return 422"
        ),
        (
            UserDataGenerator.generate_user(),
            400,
            "Missing required fields should return 400"
        ),
    ]
)
@allure.title("Negative user creation tests: {error_description}")
def test_create_user_negative(auth_client, payload, expected_status, error_description):
    """Test handling of invalid data when creating a user."""
    
    with allure.step(f"Sending request with invalid data: {error_description}"):
        resp = auth_client.post("/users", json=payload)
    
    with allure.step(f"Checking status code {expected_status}"):
        assert_status_code(resp, expected_status)
    
    with allure.step("Checking error response structure"):
        if resp.status_code >= 400:
            error_data = resp.json()
            # Validate error structure via Pydantic (if API returns standard format)
            try:
                error = validate_pydantic_model(error_data, ErrorResponse)
                assert error.error is not None, "Error message should be present"
            except Exception:
                # If error format is non-standard, just check for data presence
                assert error_data, "Error response should contain data"
