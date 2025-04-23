from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str
    email: str
    phone: str

class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    model_config = {
        "from_attributes": True
    }