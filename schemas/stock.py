from pydantic import BaseModel, PositiveInt, NonNegativeInt, ConfigDict
from datetime import datetime
from typing import Optional
from schemas.product import ProductResponse

class StockCreate(BaseModel):
    product_id: PositiveInt
    branch_id: PositiveInt
    quantity: NonNegativeInt

class StockUpdate(BaseModel):
    quantity: Optional[NonNegativeInt] = None

class StockResponse(BaseModel):
    id: int
    product_id: PositiveInt
    branch_id: PositiveInt
    quantity: NonNegativeInt
    product: ProductResponse
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)