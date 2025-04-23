from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from schemas.movement import MovementCreate, MovementResponse
from cruds import movement

router = APIRouter(prefix="/movements", tags=["Movements"])

@router.post("", response_model=MovementResponse)
def create_movement(new_movement: MovementCreate, db: Session = Depends(get_db)):
    return movement.create_movement(db, new_movement)

@router.get("", response_model=List[MovementResponse])
def get_movements(db: Session = Depends(get_db)):
    return movement.list_movements(db)