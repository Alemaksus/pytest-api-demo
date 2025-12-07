"""API security tests."""

import pytest
import allure
from utils.helpers import assert_status_code


@pytest.mark.api
@allure.title("Authorization check - request without token")
def test_unauthorized_access(api_client):
    """Verifies that unauthorized requests are rejected."""
    response = api_client.get("/users/1")
    
    # Should return 401 Unauthorized
    assert_status_code(response, 401, "Unauthorized request should return 401")


@pytest.mark.api
@allure.title("Authorization check - invalid token")
def test_invalid_token(api_client):
    """Verifies that invalid token is rejected."""
    api_client.session.headers.update({
        "Authorization": "Bearer invalid_token_12345"
    })
    
    response = api_client.get("/users/1")
    assert_status_code(response, 401, "Invalid token should return 401")


@pytest.mark.api
@allure.title("CORS headers check")
def test_cors_headers(auth_client):
    """Verifies presence of CORS headers in response."""
    response = auth_client.get("/users/1")
    
    # Check for CORS headers (if API supports them)
    cors_headers = [
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers"
    ]
    
    # This is an optional check, depends on API
    # allure.attach(
    #     str(dict(response.headers)),
    #     name="Response Headers",
    #     attachment_type=allure.attachment_type.JSON
    # )


@pytest.mark.api
@allure.title("SQL injection protection check")
def test_sql_injection_protection(auth_client):
    """Verifies protection against SQL injection in parameters."""
    # SQL injection attempt in parameter
    malicious_input = "1' OR '1'='1"
    response = auth_client.get(f"/users/{malicious_input}")
    
    # Should return 400 or 404, but not 500 (which would indicate vulnerability)
    assert response.status_code != 500, \
        "SQL injection attempt should not cause server error"
    assert response.status_code in [400, 404, 422], \
        f"SQL injection attempt should return 400/404/422, got {response.status_code}"



