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
    """Validates JSON data against JSON Schema.
    
    Args:
        instance: JSON data to validate
        schema: JSON Schema for validation
        raise_on_error: If True, raises exception on validation error
        
    Returns:
        True if validation passed successfully
        
    Raises:
        ValidationError: If validation failed and raise_on_error=True
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
    """Validates data via Pydantic model.
    
    Args:
        data: JSON data to validate
        model_class: Pydantic model class
        raise_on_error: If True, raises exception on validation error
        
    Returns:
        Validated model object
        
    Raises:
        PydanticValidationError: If validation failed and raise_on_error=True
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
    """Checks API response time.
    
    Args:
        response: Response object from requests
        max_time_ms: Maximum allowed response time in milliseconds
        
    Returns:
        True if response time is within acceptable range
    """
    elapsed_ms = response.elapsed.total_seconds() * 1000
    return elapsed_ms <= max_time_ms


def validate_status_code(
    response: requests.Response,
    expected_codes: Union[int, Iterable[int]] = 200
) -> bool:
    """Checks response status code.
    
    Args:
        response: Response object from requests
        expected_codes: Expected status code(s)
        
    Returns:
        True if status code matches expected value
    """
    if isinstance(expected_codes, int):
        expected_codes = [expected_codes]
    return response.status_code in expected_codes

