from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.movement import Movement
from models.stock import Stock
from models.user import User
from models.product import Product
from models.branch import Branch
from schemas.movement import MovementCreate
from fastapi import HTTPException


def create_movement(db: Session, movement: MovementCreate):
    """Create a stock movement between branches."""
    # Verify user exists
    user = db.query(User).filter(User.id == movement.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify product and branches exist
    product = db.query(Product).filter(Product.id == movement.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    origin_branch = db.query(Branch).filter(Branch.id == movement.origin_branch_id).first()
    if not origin_branch:
        raise HTTPException(status_code=404, detail="Origin branch not found")
    dest_branch = db.query(Branch).filter(Branch.id == movement.destination_branch_id).first()
    if not dest_branch:
        raise HTTPException(status_code=404, detail="Destination branch not found")

    # Verify stock availability
    origin_stock = db.query(Stock).filter(
        Stock.product_id == movement.product_id,
        Stock.branch_id == movement.origin_branch_id
    ).first()
    if not origin_stock or origin_stock.quantity < movement.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock at origin branch")

    # Find or create destination stock
    dest_stock = db.query(Stock).filter(
        Stock.product_id == movement.product_id,
        Stock.branch_id == movement.destination_branch_id
    ).first()
    if not dest_stock:
        dest_stock = Stock(
            product_id=movement.product_id,
            branch_id=movement.destination_branch_id,
            quantity=0
        )
        db.add(dest_stock)
        db.flush()  # Ensure dest_stock has an ID

    # Update stock quantities
    origin_stock.quantity -= movement.quantity
    dest_stock.quantity += movement.quantity

    # Create movement
    db_movement = Movement(**movement.model_dump())
    db.add(db_movement)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error registering movement")

    db.refresh(db_movement)
    return db_movement


def list_movements(db: Session):
    """Get all movements, ordered by timestamp descending."""
    return db.query(Movement).order_by(Movement.timestamp.desc()).all()