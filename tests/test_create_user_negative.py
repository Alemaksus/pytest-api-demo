"""Негативные тесты для создания пользователя."""

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
            "Пустой email должен возвращать 422"
        ),
        (
            {"email": "not-email", "role": "user"},
            422,
            "Невалидный email должен возвращать 422"
        ),
        (
            {"email": "qa@example.com", "role": "root"},
            422,
            "Неверный enum для role должен возвращать 422"
        ),
        (
            UserDataGenerator.generate_user(),
            400,
            "Отсутствие обязательных полей должно возвращать 400"
        ),
    ]
)
@allure.title("Негативные тесты создания пользователя: {error_description}")
def test_create_user_negative(auth_client, payload, expected_status, error_description):
    """Тест обработки некорректных данных при создании пользователя."""
    
    with allure.step(f"Отправка запроса с некорректными данными: {error_description}"):
        resp = auth_client.post("/users", json=payload)
    
    with allure.step(f"Проверка статус кода {expected_status}"):
        assert_status_code(resp, expected_status)
    
    with allure.step("Проверка структуры ответа об ошибке"):
        if resp.status_code >= 400:
            error_data = resp.json()
            # Валидируем структуру ошибки через Pydantic (если API возвращает стандартный формат)
            try:
                error = validate_pydantic_model(error_data, ErrorResponse)
                assert error.error is not None, "Error message should be present"
            except Exception:
                # Если формат ошибки нестандартный, просто проверяем наличие данных
                assert error_data, "Error response should contain data"
