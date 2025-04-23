from pydantic import BaseModel
from datetime import datetime


class MovementCreate(BaseModel):
    product_name: str
    quantity: int
    origin_branch: str
    destination_branch: str
    notes: str = None

class MovementResponse(MovementCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }