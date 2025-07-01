from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy
from fastapi_pagination.cursor import CursorPage
from db.base import get_db
from schemas.movement import MovementCreate, MovementResponse
from cruds import movement
from models.user import User
from utils.auth import get_current_user
from utils.logger import get_logger
from utils.pagination import CustomCursorParams


logger = get_logger(__name__)

router = APIRouter(prefix="/movements", tags=["Movements"])

@router.post("", response_model=MovementResponse, status_code=201)
def create_movement(new_movement: MovementCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a stock movement between branches."""
    new_movement.user_id = user.id  # Set user_id from authenticated user
    logger.info(f"Creating movement for product ID: {new_movement.product_id} by user ID: {user.id}")
    return movement.create_movement(db, new_movement)

@router.get("", response_model=CursorPage[MovementResponse])
def get_movements(db: Session = Depends(get_db), params: CustomCursorParams = Depends()):
    """Get all movements with cursor-based pagination."""
    logger.info(f"Fetching movements with cursor={params.cursor}, size={params.size}, order={params.order}")
    query = movement.list_movements(db)  # Ensure this returns a SQLAlchemy query
    return paginate_sqlalchemy(query, params)
