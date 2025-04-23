from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}