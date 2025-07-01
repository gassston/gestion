from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy
from fastapi_pagination.cursor import CursorPage
from sqlalchemy.orm import Session
from db.base import get_db
from schemas.user import UserCreate, UserResponse, UserUpdate
from cruds import user
from utils.auth import get_current_admin, get_current_user
from utils.logger import get_logger
from utils.pagination import CustomCursorParams

logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse, status_code=201, dependencies=[Depends(get_current_admin)])
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user (admin only)."""
    logger.info(f"Creating user: {new_user.username}")
    return user.create_user(db, new_user)

@router.get("", response_model=CursorPage[UserResponse])
def list_users(db: Session = Depends(get_db), params: CustomCursorParams = Depends()):
    """Get all users with cursor-based pagination."""
    logger.info(f"Fetching users with cursor={params.cursor}, size={params.size}, order={params.order}")
    query = user.list_users(db)
    return paginate_sqlalchemy(query, params)

@router.get("/me", response_model=UserResponse)
def get_current_user_details(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get the current user's details."""
    user = current_user["user"]
    logger.info(f"Fetching details for user: {user.username}")
    return user

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
