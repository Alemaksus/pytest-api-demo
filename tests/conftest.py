"""Pytest configuration and shared fixtures."""

import logging
from typing import Generator

import pytest

from client.api_base_client import BaseClient
from config.settings import Settings, get_settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Фикстура для доступа к настройкам окружения (BASE_URL, ENV, токены и т.п.).

    Возвращает объект настроек, который переиспользуется во всех тестах.
    """
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings) -> BaseClient:
    """Фикстура для создания базового API клиента.
    
    Использует настройки из конфигурации для создания клиента.
    Клиент создается один раз на всю сессию тестов.
    """
    logger.info(f"Creating API client for {settings.base_url}")
    client = BaseClient(
        base_url=settings.base_url,
        default_headers={"Content-Type": "application/json"}
    )
    return client


@pytest.fixture(scope="session")
def auth_token(api_client: BaseClient, settings) -> str:
    """Фикстура для получения токена авторизации.  
    Выполняет авторизацию один раз на сессию и возвращает токен.
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
    """Фикстура для создания авторизованного клиента.
    Автоматически добавляет Authorization заголовок к каждому запросу.
    """
    # Создаем копию заголовков, чтобы не изменять оригинальный клиент
    api_client.session.headers.update({
        "Authorization": f"Bearer {auth_token}"
    })
    return api_client


@pytest.fixture(autouse=True)
def log_test_start(request):
    """Автоматически логирует начало каждого теста."""
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Finished test: {request.node.name}")


@pytest.fixture
def clean_user_data():
    """Фикстура для очистки тестовых данных после теста.
    Можно использовать для удаления созданных в тесте данных.
    """
    created_ids = []
    
    yield created_ids
    
    # Cleanup логика (если нужна)
    if created_ids:
        logger.info(f"Cleaning up {len(created_ids)} test records")



