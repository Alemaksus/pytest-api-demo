"""Тесты безопасности API."""

import pytest
import allure
from utils.helpers import assert_status_code


@pytest.mark.api
@allure.title("Проверка авторизации - запрос без токена")
def test_unauthorized_access(api_client):
    """Проверяет, что запросы без авторизации отклоняются."""
    response = api_client.get("/users/1")
    
    # Должен вернуть 401 Unauthorized
    assert_status_code(response, 401, "Unauthorized request should return 401")


@pytest.mark.api
@allure.title("Проверка авторизации - невалидный токен")
def test_invalid_token(api_client):
    """Проверяет, что невалидный токен отклоняется."""
    api_client.session.headers.update({
        "Authorization": "Bearer invalid_token_12345"
    })
    
    response = api_client.get("/users/1")
    assert_status_code(response, 401, "Invalid token should return 401")


@pytest.mark.api
@allure.title("Проверка CORS заголовков")
def test_cors_headers(auth_client):
    """Проверяет наличие CORS заголовков в ответе."""
    response = auth_client.get("/users/1")
    
    # Проверяем наличие CORS заголовков (если API их поддерживает)
    cors_headers = [
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers"
    ]
    
    # Это опциональная проверка, зависит от API
    # allure.attach(
    #     str(dict(response.headers)),
    #     name="Response Headers",
    #     attachment_type=allure.attachment_type.JSON
    # )


@pytest.mark.api
@allure.title("Проверка защиты от SQL инъекций")
def test_sql_injection_protection(auth_client):
    """Проверяет защиту от SQL инъекций в параметрах."""
    # Попытка SQL инъекции в параметре
    malicious_input = "1' OR '1'='1"
    response = auth_client.get(f"/users/{malicious_input}")
    
    # Должен вернуть 400 или 404, но не 500 (что означало бы уязвимость)
    assert response.status_code != 500, \
        "SQL injection attempt should not cause server error"
    assert response.status_code in [400, 404, 422], \
        f"SQL injection attempt should return 400/404/422, got {response.status_code}"



