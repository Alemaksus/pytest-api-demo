"""API performance tests."""

import pytest
import allure
from utils.helpers import get_response_time_ms
from utils.validators import validate_response_time


@pytest.mark.slow
@pytest.mark.api
@allure.title("GET request response time check")
def test_get_user_performance(auth_client):
    """Verifies that GET request executes quickly."""
    response = auth_client.get("/users/1")
    
    response_time_ms = get_response_time_ms(response)
    allure.attach(
        f"Response time: {response_time_ms:.2f}ms",
        name="Performance Metrics",
        attachment_type=allure.attachment_type.TEXT
    )
    
    # Verify response came in less than 500ms
    assert validate_response_time(response, max_time_ms=500), \
        f"Response time {response_time_ms}ms exceeds 500ms"


@pytest.mark.slow
@pytest.mark.api
@allure.title("POST request response time check")
def test_create_user_performance(auth_client):
    """Verifies that POST request executes in reasonable time."""
    from utils.data_generators import UserDataGenerator
    
    payload = UserDataGenerator.generate_user()
    response = auth_client.post("/users", json=payload)
    
    response_time_ms = get_response_time_ms(response)
    allure.attach(
        f"Response time: {response_time_ms:.2f}ms",
        name="Performance Metrics",
        attachment_type=allure.attachment_type.TEXT
    )
    
    # POST requests may be slower, check 1 second
    assert validate_response_time(response, max_time_ms=1000), \
        f"Response time {response_time_ms}ms exceeds 1000ms"


@pytest.mark.slow
@pytest.mark.parametrize("endpoint", ["/users", "/users/1", "/health"])
@allure.title("Endpoint performance check: {endpoint}")
def test_endpoint_performance(auth_client, endpoint):
    """Verifies performance of various endpoints."""
    response = auth_client.get(endpoint)
    
    response_time_ms = get_response_time_ms(response)
    
    # Different endpoints may have different performance requirements
    max_time = 2000 if "/users" in endpoint else 1000
    
    assert validate_response_time(response, max_time_ms=max_time), \
        f"Endpoint {endpoint} response time {response_time_ms}ms exceeds {max_time}ms"



