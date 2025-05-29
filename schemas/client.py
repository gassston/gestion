from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, value):
        """Ensure name is not empty and within length limits."""
        if not value.strip():
            raise ValueError('Name cannot be empty')
        if len(value) > 100:
            raise ValueError('Name cannot exceed 100 characters')
        return value.strip()

    @field_validator('phone')
    @classmethod
    def phone_format(cls, value):
        """Ensure phone contains valid characters and length."""
        if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('Phone must contain only digits, +, -, or spaces')
        if len(value) > 20:
            raise ValueError('Phone cannot exceed 20 characters')
        return value.strip()

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @field_validator('name', check_fields=False)
    @classmethod
    def name_not_empty(cls, value):
        if value is not None:
            if not value.strip():
                raise ValueError('Name cannot be empty')
            if len(value) > 100:
                raise ValueError('Name cannot exceed 100 characters')
        return value.strip() if value else None

    @field_validator('phone', check_fields=False)
    @classmethod
    def phone_format(cls, value):
        if value is not None:
            if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                raise ValueError('Phone must contain only digits, +, -, or spaces')
            if len(value) > 20:
                raise ValueError('Phone cannot exceed 20 characters')
        return value.strip() if value else None

class ClientResponse(ClientCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)