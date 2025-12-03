"""Helper functions for tests."""

from typing import Any, Optional
import requests


def assert_status_code(
    response: requests.Response,
    expected_code: int,
    message: Optional[str] = None
) -> None:
    """Проверяет статус код ответа с понятным сообщением об ошибке.
    
    Args:
        response: Объект Response из requests
        expected_code: Ожидаемый статус код
        message: Дополнительное сообщение об ошибке
        
    Raises:
        AssertionError: Если статус код не соответствует ожидаемому
    """
    error_msg = (
        f"Expected status code {expected_code}, "
        f"but got {response.status_code}"
    )
    if message:
        error_msg += f". {message}"
    error_msg += f"\nResponse: {response.text[:500]}"
    
    assert response.status_code == expected_code, error_msg


def extract_json_field(
    response: requests.Response,
    field_path: str,
    default: Any = None
) -> Any:
    """Извлекает поле из JSON ответа по пути.
    
    Args:
        response: Объект Response из requests
        field_path: Путь к полю (например, "user.id" или "data[0].name")
        default: Значение по умолчанию, если поле не найдено
        
    Returns:
        Значение поля или default
    """
    try:
        data = response.json()
        keys = field_path.split(".")
        result = data
        for key in keys:
            if "[" in key:
                # Обработка массивов: "items[0]"
                field_name, index = key.split("[")
                index = int(index.rstrip("]"))
                result = result[field_name][index]
            else:
                result = result[key]
        return result
    except (KeyError, IndexError, TypeError, ValueError):
        return default


def get_response_time_ms(response: requests.Response) -> float:
    """Получает время ответа в миллисекундах.
    
    Args:
        response: Объект Response из requests
        
    Returns:
        Время ответа в миллисекундах
    """
    return response.elapsed.total_seconds() * 1000



