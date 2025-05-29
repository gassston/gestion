from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from db.base import get_db
from schemas.user import UserCreate, UserResponse, UserUpdate
from cruds import user
from utils.auth import get_current_admin
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse, status_code=201, dependencies=[Depends(get_current_admin)])
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user (admin only)."""
    logger.info(f"Creating user: {new_user.username}")
    return user.create_user(db, new_user)

@router.get("", response_model=Page[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """Get all users with pagination."""
    return paginate(user.list_users(db))

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID."""
    getuser = user.get_user(db, user_id)
    if not getuser:
        raise HTTPException(status_code=404, detail="User not found")
    return getuser

@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(get_current_admin)])
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    """Update a user (admin only)."""
    updated = user.update_user(db, user_id, updated_user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Updated user ID: {user_id}")
    return updated

@router.delete("/{user_id}", dependencies=[Depends(get_current_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user (admin only)."""
    deleted = user.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Deleted user ID: {user_id}")
    return {"message": "User deleted"}