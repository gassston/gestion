from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from models.user import Role

class UserCreate(BaseModel):
    username: str
    name: str
    email: Optional[EmailStr] = None
    password: str
    role: Role = Role.user

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, value):
        """Ensure username is alphanumeric and meets length requirements."""
        if not value.isalnum():
            raise ValueError('Username must be alphanumeric')
        if len(value) < 3:
            raise ValueError('Username must be at least 3 characters')
        return value

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, value):
        """Ensure name is not empty and within length limits."""
        if not value.strip():
            raise ValueError('Name cannot be empty')
        if len(value) > 100:
            raise ValueError('Name cannot exceed 100 characters')
        return value.strip()

    @field_validator('password')
    @classmethod
    def password_strength(cls, value):
        """Ensure password meets minimum length."""
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters')
        return value

    # @field_validator('role')
    # @classmethod
    # def valid_role(cls, value):
    #     """Ensure role is either 'user' or 'admin'."""
    #     if value not in ['user', 'admin']:
    #         raise ValueError('Role must be "user" or "admin"')
    #     return value

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role] = None

    @field_validator('name', check_fields=False)
    @classmethod
    def name_not_empty(cls, value):
        if value is not None:
            if not value.strip():
                raise ValueError('Name cannot be empty')
            if len(value) > 100:
                raise ValueError('Name cannot exceed 100 characters')
        return value.strip() if value else None

    @field_validator('password', check_fields=False)
    @classmethod
    def password_strength(cls, value):
        if value is not None and len(value) < 8:
            raise ValueError('Password must be at least 8 characters')
        return value

    # @field_validator('role', check_fields=False)
    # @classmethod
    # def valid_role(cls, value):
    #     if value not in ['user', 'admin']:
    #         raise ValueError('Role must be "user" or "admin"')
    #     return value

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: Optional[EmailStr]
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
