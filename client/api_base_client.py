"""Базовый API клиент с логированием, retry и обработкой ошибок."""

import logging
import time
from typing import Optional, Dict, Any
import requests
from requests.exceptions import Timeout, RequestException

from client.exceptions import (
    APIRequestException,
    APITimeoutException,
    APIRetryException
)

logger = logging.getLogger(__name__)


class BaseClient:
    """Базовый клиент для REST API с единым методом request,
    поддержкой сессий, заголовков, логирования и обработкой ошибок.
    
    Features:
    - Логирование всех запросов и ответов
    - Retry механизм для нестабильных запросов
    - Кастомные исключения для лучшей обработки ошибок
    - Поддержка таймаутов
    """

    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        retry_count: int = 3,
        retry_delay: float = 1.0
    ):
        """Инициализация API клиента.
        
        Args:
            base_url: Базовый URL API
            default_headers: Заголовки по умолчанию для всех запросов
            timeout: Таймаут запросов в секундах
            retry_count: Количество попыток при ошибке
            retry_delay: Задержка между попытками в секундах
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        
        logger.info(
            f"Initialized BaseClient: base_url={self.base_url}, "
            f"timeout={self.timeout}, retry_count={self.retry_count}"
        )

    def _build_url(self, path: str) -> str:
        """Строит полный URL из базового URL и пути."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def _log_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> None:
        """Логирует детали запроса."""
        logger.info(f"→ {method} {url}")
        if params:
            logger.debug(f"  Params: {params}")
        if json_data:
            logger.debug(f"  Body: {json_data}")
        if headers:
            logger.debug(f"  Headers: {dict(headers)}")

    def _log_response(self, response: requests.Response) -> None:
        """Логирует детали ответа."""
        elapsed_ms = response.elapsed.total_seconds() * 1000
        logger.info(
            f"← {response.status_code} {response.reason} "
            f"({elapsed_ms:.2f}ms)"
        )
        try:
            logger.debug(f"  Response: {response.text[:500]}")
        except Exception:
            logger.debug("  Response: (unable to log)")

    def request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        retry: bool = True,
        **kwargs
    ) -> requests.Response:
        """Выполняет HTTP запрос с логированием и retry механизмом.
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE, etc.)
            path: Путь эндпоинта
            json: JSON данные для тела запроса
            params: Query параметры
            headers: Дополнительные заголовки
            retry: Включить ли retry механизм
            **kwargs: Дополнительные параметры для requests
            
        Returns:
            Объект Response из requests
            
        Raises:
            APITimeoutException: При таймауте запроса
            APIRequestException: При ошибке HTTP запроса
            APIRetryException: Когда все попытки retry исчерпаны
        """
        url = self._build_url(path)

        # Собираем финальные заголовки
        final_headers = self.default_headers.copy()
        if headers:
            final_headers.update(headers)

        # Логируем запрос
        self._log_request(method, url, final_headers, json, params)

        # Retry механизм
        last_exception = None
        for attempt in range(1, (self.retry_count + 1) if retry else 2):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=json,
                    params=params,
                    headers=final_headers,
                    timeout=self.timeout,
                    **kwargs
                )

                # Логируем ответ
                self._log_response(response)

                # Обработка ошибок сервера
                if response.status_code >= 500:
                    error_msg = (
                        f"Server error {response.status_code}: "
                        f"{response.text[:200]}"
                    )
                    if retry and attempt < self.retry_count:
                        logger.warning(
                            f"Server error, retrying ({attempt}/{self.retry_count})..."
                        )
                        time.sleep(self.retry_delay)
                        continue
                    raise APIRequestException(
                        error_msg,
                        status_code=response.status_code,
                        response_text=response.text
                    )

                return response

            except Timeout as e:
                last_exception = e
                if retry and attempt < self.retry_count:
                    logger.warning(
                        f"Request timeout, retrying ({attempt}/{self.retry_count})..."
                    )
                    time.sleep(self.retry_delay)
                    continue
                raise APITimeoutException(
                    f"Request timeout after {self.timeout}s: {str(e)}"
                ) from e

            except RequestException as e:
                last_exception = e
                if retry and attempt < self.retry_count:
                    logger.warning(
                        f"Request failed, retrying ({attempt}/{self.retry_count}): {str(e)}"
                    )
                    time.sleep(self.retry_delay)
                    continue
                raise APIRequestException(
                    f"Request failed: {str(e)}"
                ) from e

        # Если все попытки исчерпаны
        raise APIRetryException(
            f"All {self.retry_count} retry attempts failed. "
            f"Last error: {str(last_exception)}"
        )

    # Удобные короткие методы
    def get(self, path: str, **kwargs) -> requests.Response:
        """GET запрос."""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """POST запрос."""
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """PUT запрос."""
        return self.request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """PATCH запрос."""
        return self.request("PATCH", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """DELETE запрос."""
        return self.request("DELETE", path, **kwargs)
