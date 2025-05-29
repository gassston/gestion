from pydantic import BaseModel, PositiveInt, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class MovementCreate(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt
    origin_branch_id: PositiveInt
    destination_branch_id: PositiveInt
    user_id: PositiveInt
    notes: Optional[str] = None

    @field_validator('destination_branch_id', check_fields=True)
    @classmethod
    def branches_different(cls, value, values):
        """Ensure origin and destination branches are different."""
        if values.data.get('origin_branch_id') == value:
            raise ValueError('Origin and destination branches must be different')
        return value

class MovementResponse(MovementCreate):
    id: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
