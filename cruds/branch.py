from sqlalchemy.orm import Session
from models.branch import Branch
from models.stock import Stock
from models.movement import Movement
from schemas.branch import BranchCreate, BranchUpdate
from fastapi import HTTPException

def get_branches(db: Session):
    """Get all branches."""
    return db.query(Branch).order_by(Branch.id.asc())

def get_branch(db: Session, branch_id: int):
    """Get a branch by ID."""
    return db.query(Branch).filter(Branch.id == branch_id).first()

def create_branch(db: Session, branch: BranchCreate):
    """Create a new branch."""
    existing_branch = db.query(Branch).filter(Branch.name == branch.name).first()
    if existing_branch:
        raise HTTPException(status_code=400, detail="Branch name already exists")
    db_branch = Branch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def update_branch(db: Session, branch_id: int, branch_data: BranchUpdate):
    """Update a branch."""
    branch = get_branch(db, branch_id)
    if not branch:
        return None
    update_data = branch_data.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"]:
        existing_branch = db.query(Branch).filter(Branch.name == update_data["name"], Branch.id != branch_id).first()
        if existing_branch:
            raise HTTPException(status_code=400, detail="Branch name already exists")
    for key, value in update_data.items():
        setattr(branch, key, value)
    db.commit()
    db.refresh(branch)
    return branch

def delete_branch(db: Session, branch_id: int):
    """Delete a branch."""
    branch = get_branch(db, branch_id)
    if not branch:
        return False
    # Check for associated stock or movements
    if db.query(Stock).filter(Stock.branch_id == branch_id).first() or \
       db.query(Movement).filter((Movement.origin_branch_id == branch_id) | (Movement.destination_branch_id == branch_id)).first():
        raise HTTPException(status_code=400, detail="Cannot delete branch with associated stock or movements")
    db.delete(branch)
    db.commit()
    return True