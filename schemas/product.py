from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, List

class ProductCreate(BaseModel):
    name: str
    vintage: Optional[int] = None
    region: Optional[str] = None
    grape_variety: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, value):
        """Ensure wine name is not empty and within length limits."""
        if not value.strip():
            raise ValueError('Name cannot be empty')
        if len(value) > 100:
            raise ValueError('Name cannot exceed 100 characters')
        return value.strip()

    @field_validator('vintage')
    @classmethod
    def valid_vintage(cls, value):
        """Ensure vintage is a valid year (e.g., between 1900 and current year)."""
        if value is not None:
            current_year = datetime.now().year
            if not (1900 <= value <= current_year):
                raise ValueError(f'Vintage must be between 1900 and {current_year}')
        return value

    @field_validator('region')
    @classmethod
    def region_length(cls, value):
        """Ensure region is within length limits."""
        if value and len(value) > 100:
            raise ValueError('Region cannot exceed 100 characters')
        return value.strip() if value else value

    @field_validator('grape_variety')
    @classmethod
    def grape_variety_length(cls, value):
        """Ensure grape variety is within length limits."""
        if value and len(value) > 100:
            raise ValueError('Grape variety cannot exceed 100 characters')
        return value.strip() if value else value

class ProductUpdate(ProductCreate):
    name: Optional[str] = None
    vintage: Optional[int] = None
    region: Optional[str] = None
    grape_variety: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    vintage: Optional[int]
    region: Optional[str]
    grape_variety: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    next_cursor: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)