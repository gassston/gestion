from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    name: str
    email: Optional[EmailStr] = None
    password: str
    role: str = "user"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: Optional[EmailStr]
    role: str

    model_config = {"from_attributes": True}
