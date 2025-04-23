from pydantic import BaseModel

class BranchBase(BaseModel):
    name: str

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BranchBase):
    pass

class BranchResponse(BranchBase):
    id: int

    model_config = {"from_attributes": True}