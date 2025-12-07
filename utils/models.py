"""Pydantic models for API response validation."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class CompanyModel(BaseModel):
    """Company model."""
    name: str = Field(..., description="Company name")
    size: int = Field(..., gt=0, description="Number of employees")
    
    @field_validator('size')
    @classmethod
    def validate_size(cls, v: int) -> int:
        """Validates that company size is positive."""
        if v <= 0:
            raise ValueError("Company size must be positive")
        return v


class UserModel(BaseModel):
    """User model for API response validation."""
    id: str = Field(..., description="Unique user identifier")
    name: Optional[str] = Field(None, description="User first name")
    surname: Optional[str] = Field(None, description="User last name")
    email: EmailStr = Field(..., description="User email")
    role: str = Field(..., description="User role")
    company: Optional[CompanyModel] = Field(None, description="User company")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validates that role is valid."""
        valid_roles = ["user", "admin", "moderator"]
        if v not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return v


class CreateUserRequest(BaseModel):
    """Model for creating a user."""
    name: str = Field(..., min_length=1, description="User first name")
    surname: str = Field(..., min_length=1, description="User last name")
    email: EmailStr = Field(..., description="User email")
    company: CompanyModel = Field(..., description="User company")


class ErrorResponse(BaseModel):
    """Model for API errors."""
    error: str = Field(..., description="Error message")
    code: Optional[int] = Field(None, description="Error code")
    details: Optional[dict] = Field(None, description="Additional error details")



