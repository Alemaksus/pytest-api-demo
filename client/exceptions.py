"""Custom exceptions for API client."""

from typing import Optional


class APIException(Exception):
    """Base exception for API errors."""
    pass


class APIRequestException(APIException):
    """Exception for HTTP request errors."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None
    ):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)


class APITimeoutException(APIException):
    """Exception for request timeouts."""
    pass


class APIValidationException(APIException):
    """Exception for response validation errors."""
    pass


class APIRetryException(APIException):
    """Exception when all retry attempts are exhausted."""
    pass



