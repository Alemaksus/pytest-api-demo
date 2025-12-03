"""Settings and configuration management for different environments."""

import os
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


class Settings:
    """Класс для управления настройками проекта.
    
    Поддерживает разные окружения (dev, staging, prod) через переменную ENV.
    Все настройки можно переопределить через переменные окружения.
    """
    
    def __init__(self):
        # Окружение (dev, staging, prod)
        self.env: str = os.getenv("ENV", "dev")
        
        # Базовый URL API
        self.base_url: str = os.getenv(
            "BASE_URL",
            self._get_default_url()
        )
        
        # Таймаут для запросов (секунды)
        self.timeout: int = int(os.getenv("TIMEOUT", "10"))
        
        # Уровень логирования
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Настройки авторизации
        self.auth_username: Optional[str] = os.getenv("AUTH_USERNAME")
        self.auth_password: Optional[str] = os.getenv("AUTH_PASSWORD")
        self.auth_token: Optional[str] = os.getenv("AUTH_TOKEN")
        
        # Настройки для Allure
        self.allure_results_dir: str = os.getenv(
            "ALLURE_RESULTS_DIR",
            "allure-results"
        )
        
        # Retry настройки
        self.retry_count: int = int(os.getenv("RETRY_COUNT", "3"))
        self.retry_delay: float = float(os.getenv("RETRY_DELAY", "1.0"))
    
    def _get_default_url(self) -> str:
        """Возвращает URL по умолчанию в зависимости от окружения."""
        urls = {
            "dev": "https://api-dev.example.com",
            "staging": "https://api-staging.example.com",
            "prod": "https://api.example.com"
        }
        return urls.get(self.env, urls["dev"])
    
    def __repr__(self) -> str:
        return f"Settings(env={self.env}, base_url={self.base_url})"


# Глобальный экземпляр настроек
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Получить глобальный экземпляр настроек (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings



