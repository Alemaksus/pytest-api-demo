# conftest.py
import pytest
import requests


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = 5

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs):
        return self.session.get(self._url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, **kwargs):
        return self.session.post(self._url(path), timeout=self.timeout, **kwargs)


@pytest.fixture(scope="session")
def api_client():
    return ApiClient("https://api.example.com")


@pytest.fixture(scope="session")
def auth_token(api_client):
    resp = api_client.post("/auth", json={"user": "test", "password": "pass"})
    resp.raise_for_status()
    return resp.json()["token"]


@pytest.fixture
def auth_client(api_client, auth_token):
    # клиент, который автоматически прокидывает авторизационный заголовок
    api_client.session.headers.update({"Authorization": f"Bearer {auth_token}"})
    return api_client
