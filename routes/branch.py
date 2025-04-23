from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from cruds import branch as crud_branch
from schemas.branch import BranchCreate, BranchResponse, BranchUpdate

router = APIRouter(prefix="/branches", tags=["Branches"])

@router.get("", response_model=list[BranchResponse])
def list_branches(db: Session = Depends(get_db)):
    return crud_branch.get_branches(db)

@router.get("/{branch_id}", response_model=BranchResponse)
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = crud_branch.get_branch(db, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch

@router.post("", response_model=BranchResponse)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return crud_branch.create_branch(db, branch)

@router.put("/{branch_id}", response_model=BranchResponse)
def update_branch(branch_id: int, branch: BranchUpdate, db: Session = Depends(get_db)):
    updated = crud_branch.update_branch(db, branch_id, branch)
    if not updated:
        raise HTTPException(status_code=404, detail="Branch not found")
    return updated

@router.delete("/{branch_id}", response_model=BranchResponse)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    deleted = crud_branch.delete_branch(db, branch_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Branch not found")
    return deleted
