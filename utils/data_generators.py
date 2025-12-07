"""Data generators for test data using Faker."""

from faker import Faker
from typing import Dict, Any, Optional

fake = Faker()


class UserDataGenerator:
    """Test data generator for users."""
    
    @staticmethod
    def generate_user(
        email: Optional[str] = None,
        name: Optional[str] = None,
        role: str = "user"
    ) -> Dict[str, Any]:
        """Generates user data.
        
        Args:
            email: User email (if not provided, generated automatically)
            name: User first name (if not provided, generated automatically)
            role: User role (user, admin)
            
        Returns:
            Dictionary with user data
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
        """Generates an invalid email."""
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
        """Returns an empty string."""
        return ""


def generate_random_email() -> str:
    """Generates a random valid email.
    
    Returns:
        Random email address
    """
    return fake.email()


def generate_random_string(length: int = 10) -> str:
    """Generates a random string.
    
    Args:
        length: String length
        
    Returns:
        Random string
    """
    return fake.pystr(min_chars=length, max_chars=length)



