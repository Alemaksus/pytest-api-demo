"""Data generators for test data using Faker."""

from faker import Faker
from typing import Dict, Any, Optional

fake = Faker()


class UserDataGenerator:
    """Генератор тестовых данных для пользователей."""
    
    @staticmethod
    def generate_user(
        email: Optional[str] = None,
        name: Optional[str] = None,
        role: str = "user"
    ) -> Dict[str, Any]:
        """Генерирует данные пользователя.
        
        Args:
            email: Email пользователя (если не указан, генерируется автоматически)
            name: Имя пользователя (если не указано, генерируется автоматически)
            role: Роль пользователя (user, admin)
            
        Returns:
            Словарь с данными пользователя
        """
        return {
            "name": name or fake.first_name(),
            "surname": fake.last_name(),
            "email": email or fake.email(),
            "role": role,
            "company": {
                "name": fake.company(),
                "size": fake.random_int(min=1, max=10000)
            }
        }
    
    @staticmethod
    def generate_invalid_email() -> str:
        """Генерирует невалидный email."""
        invalid_emails = [
            "not-an-email",
            "@example.com",
            "user@",
            "user@.com",
            "user..name@example.com",
            "user@example",
        ]
        return fake.random.choice(invalid_emails)
    
    @staticmethod
    def generate_empty_string() -> str:
        """Возвращает пустую строку."""
        return ""


def generate_random_email() -> str:
    """Генерирует случайный валидный email.
    
    Returns:
        Случайный email адрес
    """
    return fake.email()


def generate_random_string(length: int = 10) -> str:
    """Генерирует случайную строку.
    
    Args:
        length: Длина строки
        
    Returns:
        Случайная строка
    """
    return fake.pystr(min_chars=length, max_chars=length)



