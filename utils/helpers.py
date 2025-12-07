"""Helper functions for tests."""

from typing import Any, Optional
import requests


def assert_status_code(
    response: requests.Response,
    expected_code: int,
    message: Optional[str] = None
) -> None:
    """Checks response status code with a clear error message.
    
    Args:
        response: Response object from requests
        expected_code: Expected status code
        message: Additional error message
        
    Raises:
        AssertionError: If status code does not match expected value
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
    """Extracts field from JSON response by path.
    
    Args:
        response: Response object from requests
        field_path: Path to field (e.g., "user.id" or "data[0].name")
        default: Default value if field is not found
        
    Returns:
        Field value or default
    """
    try:
        data = response.json()
        keys = field_path.split(".")
        result = data
        for key in keys:
            if "[" in key:
                # Handle arrays: "items[0]"
                field_name, index = key.split("[")
                index = int(index.rstrip("]"))
                result = result[field_name][index]
            else:
                result = result[key]
        return result
    except (KeyError, IndexError, TypeError, ValueError):
        return default


def get_response_time_ms(response: requests.Response) -> float:
    """Gets response time in milliseconds.
    
    Args:
        response: Response object from requests
        
    Returns:
        Response time in milliseconds
    """
    return response.elapsed.total_seconds() * 1000



