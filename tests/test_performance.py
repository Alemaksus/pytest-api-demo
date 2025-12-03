"""Тесты производительности API."""

import pytest
import allure
from utils.helpers import get_response_time_ms
from utils.validators import validate_response_time


@pytest.mark.slow
@pytest.mark.api
@allure.title("Проверка времени ответа GET запроса")
def test_get_user_performance(auth_client):
    """Проверяет, что GET запрос выполняется быстро."""
    response = auth_client.get("/users/1")
    
    response_time_ms = get_response_time_ms(response)
    allure.attach(
        f"Response time: {response_time_ms:.2f}ms",
        name="Performance Metrics",
        attachment_type=allure.attachment_type.TEXT
    )
    
    # Проверяем, что ответ пришел менее чем за 500мс
    assert validate_response_time(response, max_time_ms=500), \
        f"Response time {response_time_ms}ms exceeds 500ms"


@pytest.mark.slow
@pytest.mark.api
@allure.title("Проверка времени ответа POST запроса")
def test_create_user_performance(auth_client):
    """Проверяет, что POST запрос выполняется в разумное время."""
    from utils.data_generators import UserDataGenerator
    
    payload = UserDataGenerator.generate_user()
    response = auth_client.post("/users", json=payload)
    
    response_time_ms = get_response_time_ms(response)
    allure.attach(
        f"Response time: {response_time_ms:.2f}ms",
        name="Performance Metrics",
        attachment_type=allure.attachment_type.TEXT
    )
    
    # POST запросы могут быть медленнее, проверяем 1 секунду
    assert validate_response_time(response, max_time_ms=1000), \
        f"Response time {response_time_ms}ms exceeds 1000ms"


@pytest.mark.slow
@pytest.mark.parametrize("endpoint", ["/users", "/users/1", "/health"])
@allure.title("Проверка производительности эндпоинта: {endpoint}")
def test_endpoint_performance(auth_client, endpoint):
    """Проверяет производительность различных эндпоинтов."""
    response = auth_client.get(endpoint)
    
    response_time_ms = get_response_time_ms(response)
    
    # Разные эндпоинты могут иметь разные требования к производительности
    max_time = 2000 if "/users" in endpoint else 1000
    
    assert validate_response_time(response, max_time_ms=max_time), \
        f"Endpoint {endpoint} response time {response_time_ms}ms exceeds {max_time}ms"



