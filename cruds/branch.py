from sqlalchemy.orm import Session
from models.branch import Branch
from schemas.branch import BranchCreate, BranchUpdate

def get_branches(db: Session):
    return db.query(Branch).all()

def get_branch(db: Session, branch_id: int):
    return db.query(Branch).filter(Branch.id == branch_id).first()

def create_branch(db: Session, branch: BranchCreate):
    db_branch = Branch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def update_branch(db: Session, branch_id: int, branch_data: BranchUpdate):
    branch = get_branch(db, branch_id)
    if not branch:
        return None
    for key, value in branch_data.model_dump().items():
        setattr(branch, key, value)
    db.commit()
    db.refresh(branch)
    return branch

def delete_branch(db: Session, branch_id: int):
    branch = get_branch(db, branch_id)
    if not branch:
        return None
    db.delete(branch)
    db.commit()
    return branch
