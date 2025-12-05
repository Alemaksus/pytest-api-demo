"""Validators for API responses."""

import time
from typing import Any, Dict, Iterable, Type, Union

import requests
from jsonschema import ValidationError, validate
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError


def validate_json_schema(
    instance: Dict[str, Any],
    schema: Dict[str, Any],
    raise_on_error: bool = True
) -> bool:
    """Валидирует JSON данные по JSON Schema.
    
    Args:
        instance: JSON данные для валидации
        schema: JSON Schema для проверки
        raise_on_error: Если True, выбрасывает исключение при ошибке валидации
        
    Returns:
        True если валидация прошла успешно
        
    Raises:
        ValidationError: Если валидация не прошла и raise_on_error=True
    """
    try:
        validate(instance=instance, schema=schema)
        return True
    except ValidationError as e:
        if raise_on_error:
            raise ValidationError(
                f"JSON Schema validation failed: {e.message}\n"
                f"Path: {'.'.join(str(p) for p in e.path)}"
            ) from e
        return False


def validate_pydantic_model(
    data: Dict[str, Any],
    model_class: Type[BaseModel],
    raise_on_error: bool = True
) -> BaseModel:
    """Валидирует данные через Pydantic модель.
    
    Args:
        data: JSON данные для валидации
        model_class: Класс Pydantic модели
        raise_on_error: Если True, выбрасывает исключение при ошибке валидации
        
    Returns:
        Валидированный объект модели
        
    Raises:
        PydanticValidationError: Если валидация не прошла и raise_on_error=True
    """
    try:
        return model_class(**data)
    except PydanticValidationError as e:
        if raise_on_error:
            raise PydanticValidationError(
                f"Pydantic validation failed for {model_class.__name__}: {e}"
            ) from e
        raise


def validate_response_time(
    response: requests.Response,
    max_time_ms: float = 1000.0
) -> bool:
    """Проверяет время ответа API.
    
    Args:
        response: Объект Response из requests
        max_time_ms: Максимальное допустимое время ответа в миллисекундах
        
    Returns:
        True если время ответа в пределах нормы
    """
    elapsed_ms = response.elapsed.total_seconds() * 1000
    return elapsed_ms <= max_time_ms


def validate_status_code(
    response: requests.Response,
    expected_codes: Union[int, Iterable[int]] = 200
) -> bool:
    """Проверяет статус код ответа.
    
    Args:
        response: Объект Response из requests
        expected_codes: Ожидаемый код(ы) статуса
        
    Returns:
        True если статус код соответствует ожидаемому
    """
    if isinstance(expected_codes, int):
        expected_codes = [expected_codes]
    return response.status_code in expected_codes

