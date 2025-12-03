"""Pydantic models for API response validation."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class CompanyModel(BaseModel):
    """Модель компании."""
    name: str = Field(..., description="Название компании")
    size: int = Field(..., gt=0, description="Количество сотрудников")
    
    @field_validator('size')
    @classmethod
    def validate_size(cls, v: int) -> int:
        """Проверяет, что размер компании положительный."""
        if v <= 0:
            raise ValueError("Company size must be positive")
        return v


class UserModel(BaseModel):
    """Модель пользователя для валидации ответов API."""
    id: str = Field(..., description="Уникальный идентификатор пользователя")
    name: Optional[str] = Field(None, description="Имя пользователя")
    surname: Optional[str] = Field(None, description="Фамилия пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    role: str = Field(..., description="Роль пользователя")
    company: Optional[CompanyModel] = Field(None, description="Компания пользователя")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Проверяет, что роль валидна."""
        valid_roles = ["user", "admin", "moderator"]
        if v not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return v


class CreateUserRequest(BaseModel):
    """Модель для создания пользователя."""
    name: str = Field(..., min_length=1, description="Имя пользователя")
    surname: str = Field(..., min_length=1, description="Фамилия пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    company: CompanyModel = Field(..., description="Компания пользователя")


class ErrorResponse(BaseModel):
    """Модель для ошибок API."""
    error: str = Field(..., description="Сообщение об ошибке")
    code: Optional[int] = Field(None, description="Код ошибки")
    details: Optional[dict] = Field(None, description="Дополнительные детали ошибки")



