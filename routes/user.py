from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.base import get_db
from schemas.user import UserCreate, UserResponse, UserUpdate
from cruds import user

router = APIRouter(prefix="/users", tags=["User"])

@router.post("", response_model=UserResponse)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    return user.create_user(db, new_user)

@router.get("", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return user.list_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    getuser = user.get_user(db, user_id)
    if not getuser:
        raise HTTPException(status_code=404, detail="User not found")
    return getuser

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    updated = user.update_user(db, user_id, updated_user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = user.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}