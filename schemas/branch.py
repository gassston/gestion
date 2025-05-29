from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class BranchCreate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, value):
        """Ensure branch name is not empty and within length limits."""
        if not value.strip():
            raise ValueError('Name cannot be empty')
        if len(value) > 100:
            raise ValueError('Name cannot exceed 100 characters')
        return value.strip()

class BranchUpdate(BaseModel):
    name: Optional[str] = None

    @field_validator('name', check_fields=False)
    @classmethod
    def name_not_empty(cls, value):
        if value is not None:
            if not value.strip():
                raise ValueError('Name cannot be empty')
            if len(value) > 100:
                raise ValueError('Name cannot exceed 100 characters')
        return value.strip() if value else None

class BranchResponse(BranchCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)