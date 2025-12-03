"""Custom exceptions for API client."""


class APIException(Exception):
    """Базовое исключение для API ошибок."""
    pass


class APIRequestException(APIException):
    """Исключение для ошибок HTTP запросов."""
    
    def __init__(
        self,
        message: str,
        status_code: int = None,
        response_text: str = None
    ):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)


class APITimeoutException(APIException):
    """Исключение для таймаутов запросов."""
    pass


class APIValidationException(APIException):
    """Исключение для ошибок валидации ответов."""
    pass


class APIRetryException(APIException):
    """Исключение когда все попытки retry исчерпаны."""
    pass



