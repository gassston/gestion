from pydantic import BaseModel
from schemas.product import ProductResponse

class StockBase(BaseModel):
    product_id: int
    branch_id: int
    quantity: int

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    quantity: int

class StockResponse(BaseModel):
    id: int
    quantity: int
    product: ProductResponse

    model_config = {"from_attributes": True}