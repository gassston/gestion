from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, paginate
from db.base import get_db
from schemas.branch import BranchCreate, BranchUpdate, BranchResponse
from cruds import branch as crud_branch
from utils.auth import get_current_admin
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/branches", tags=["Branches"])

@router.get("", response_model=Page[BranchResponse])
def list_branches(db: Session = Depends(get_db)):
    """Get all branches with pagination."""
    return paginate(crud_branch.get_branches(db))

@router.get("/{branch_id}", response_model=BranchResponse)
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    """Get a branch by ID."""
    branch = crud_branch.get_branch(db, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch

@router.post("", response_model=BranchResponse, status_code=201, dependencies=[Depends(get_current_admin)])
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    """Create a new branch (admin only)."""
    logger.info(f"Creating branch: {branch.name}")
    return crud_branch.create_branch(db, branch)

@router.put("/{branch_id}", response_model=BranchResponse, dependencies=[Depends(get_current_admin)])
def update_branch(branch_id: int, branch: BranchUpdate, db: Session = Depends(get_db)):
    """Update a branch (admin only)."""
    updated = crud_branch.update_branch(db, branch_id, branch)
    if not updated:
        raise HTTPException(status_code=404, detail="Branch not found")
    logger.info(f"Updated branch ID: {branch_id}")
    return updated

@router.delete("/{branch_id}", dependencies=[Depends(get_current_admin)])
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    """Delete a branch (admin only)."""
    deleted = crud_branch.delete_branch(db, branch_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Branch not found")
    logger.info(f"Deleted branch ID: {branch_id}")
    return {"message": "Branch deleted"}
