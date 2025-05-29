from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, value):
        """Ensure product name is not empty and within length limits."""
        if not value.strip():
            raise ValueError('Name cannot be empty')
        if len(value) > 100:
            raise ValueError('Name cannot exceed 100 characters')
        return value.strip()

class ProductUpdate(ProductCreate):
    name: Optional[str] = None
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)