"""Base API client with logging, retry mechanism, and error handling."""

import time
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException, Timeout

from client.exceptions import (APIRequestException, APIRetryException,
                               APITimeoutException)
from utils.logging import get_logger

logger = get_logger(__name__)


class BaseClient:
    """Base client for REST API with unified request method,
    session support, headers, logging, and error handling.
    
    Features:
    - Logging of all requests and responses
    - Retry mechanism for unstable requests
    - Custom exceptions for better error handling
    - Timeout support
    """

    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        retry_count: int = 3,
        retry_delay: float = 1.0
    ):
        """Initialize API client.
        
        Args:
            base_url: Base API URL
            default_headers: Default headers for all requests
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts on error
            retry_delay: Delay between retry attempts in seconds
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
        """Builds full URL from base URL and path."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def _log_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> None:
        """Logs request details."""
        logger.info(f"→ {method} {url}")
        if params:
            logger.debug(f"  Params: {params}")
        if json_data:
            logger.debug(f"  Body: {json_data}")
        if headers:
            logger.debug(f"  Headers: {dict(headers)}")

    def _log_response(self, response: requests.Response) -> None:
        """Logs response details."""
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
        """Executes HTTP request with logging and retry mechanism.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: Endpoint path
            json: JSON data for request body
            params: Query parameters
            headers: Additional headers
            retry: Enable retry mechanism
            **kwargs: Additional parameters for requests
            
        Returns:
            Response object from requests
            
        Raises:
            APITimeoutException: On request timeout
            APIRequestException: On HTTP request error
            APIRetryException: When all retry attempts are exhausted
        """
        url = self._build_url(path)

        # Assemble final headers
        final_headers = self.default_headers.copy()
        if headers:
            final_headers.update(headers)

        # Log request
        self._log_request(method, url, final_headers, json, params)

        # Retry mechanism
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

                # Log response
                self._log_response(response)

                # Handle server errors
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

        # If all attempts are exhausted
        raise APIRetryException(
            f"All {self.retry_count} retry attempts failed. "
            f"Last error: {str(last_exception)}"
        )

    # Convenient shorthand methods
    def get(self, path: str, **kwargs) -> requests.Response:
        """GET request."""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """POST request."""
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """PUT request."""
        return self.request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """PATCH request."""
        return self.request("PATCH", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """DELETE request."""
        return self.request("DELETE", path, **kwargs)
