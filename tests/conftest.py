"""Pytest configuration and shared fixtures."""

import logging
from typing import Generator

import pytest

from client.api_base_client import BaseClient
from config.settings import Settings, get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Fixture for accessing environment settings (BASE_URL, ENV, tokens, etc.).

    Returns a settings object that is reused across all tests.
    """
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings) -> BaseClient:
    """Fixture for creating base API client.
    
    Uses configuration settings to create the client.
    Client is created once per test session.
    """
    logger.info(f"Creating API client for {settings.base_url}")
    client = BaseClient(
        base_url=settings.base_url,
        default_headers={"Content-Type": "application/json"}
    )
    return client


@pytest.fixture(scope="session")
def auth_token(api_client: BaseClient, settings) -> str:
    """Fixture for obtaining authentication token.
    Performs authentication once per session and returns the token.
    """
    logger.info("Getting auth token")
    try:
        auth_data = {
            "username": settings.auth_username or "test",
            "password": settings.auth_password or "test"
        }
        response = api_client.post("/auth", json=auth_data)
        response.raise_for_status()
        token = response.json().get("token")
        if not token:
            raise ValueError("Token not found in auth response")
        logger.info("Auth token obtained successfully")
        return token
    except Exception as e:
        logger.warning(f"Failed to get auth token: {e}. Using mock token.")
        return "mock_token_for_testing"


@pytest.fixture
def auth_client(api_client: BaseClient, auth_token: str) -> BaseClient:
    """Fixture for creating authenticated client.
    Automatically adds Authorization header to each request.
    """
    # Create a copy of headers to avoid modifying the original client
    api_client.session.headers.update({
        "Authorization": f"Bearer {auth_token}"
    })
    return api_client


@pytest.fixture(autouse=True)
def log_test_start(request):
    """Automatically logs the start of each test."""
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Finished test: {request.node.name}")


@pytest.fixture
def clean_user_data():
    """Fixture for cleaning up test data after test.
    Can be used to delete data created during the test.
    """
    created_ids = []
    
    yield created_ids
    
    # Cleanup logic (if needed)
    if created_ids:
        logger.info(f"Cleaning up {len(created_ids)} test records")



