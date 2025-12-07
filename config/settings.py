"""Settings and configuration management for different environments."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


class Settings:
    """Class for managing project settings.
    
    Supports different environments (dev, staging, prod) via ENV variable.
    All settings can be overridden via environment variables.
    """
    
    def __init__(self):
        # Environment (dev, staging, prod)
        self.env: str = os.getenv("ENV", "dev")
        
        # Base API URL
        self.base_url: str = os.getenv(
            "BASE_URL",
            self._get_default_url()
        )
        
        # Request timeout (seconds)
        self.timeout: int = int(os.getenv("TIMEOUT", "10"))
        
        # Logging level
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Authentication settings
        self.auth_username: Optional[str] = os.getenv("AUTH_USERNAME")
        self.auth_password: Optional[str] = os.getenv("AUTH_PASSWORD")
        self.auth_token: Optional[str] = os.getenv("AUTH_TOKEN")
        
        # Allure settings
        self.allure_results_dir: str = os.getenv(
            "ALLURE_RESULTS_DIR",
            "allure-results"
        )
        
        # Retry settings
        self.retry_count: int = int(os.getenv("RETRY_COUNT", "3"))
        self.retry_delay: float = float(os.getenv("RETRY_DELAY", "1.0"))
    
    def _get_default_url(self) -> str:
        """Returns default URL based on environment."""
        urls = {
            "dev": "https://api-dev.example.com",
            "staging": "https://api-staging.example.com",
            "prod": "https://api.example.com"
        }
        return urls.get(self.env, urls["dev"])
    
    def __repr__(self) -> str:
        return f"Settings(env={self.env}, base_url={self.base_url})"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings



