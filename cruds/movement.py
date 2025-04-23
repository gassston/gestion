from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.movement import Movement
from models.stock import Stock
from schemas.movement import MovementCreate
from fastapi import HTTPException

def create_movement(db: Session, movement: MovementCreate):
    # Paso 1: Buscar stock en sucursal origen
    origin_stock = db.query(Stock).filter(
        Stock.product_name == movement.product_name,
        Stock.branch == movement.origin_branch
    ).first()

    if not origin_stock or origin_stock.quantity < movement.quantity:
        raise HTTPException(status_code=400, detail="Stock insuficiente en la sucursal de origen.")

    # Paso 2: Buscar o crear stock en sucursal destino
    dest_stock = db.query(Stock).filter(
        Stock.product_name == movement.product_name,
        Stock.branch == movement.destination_branch
    ).first()

    if not dest_stock:
        dest_stock = Stock(
            product_name=movement.product_name,
            quantity=0,
            branch=movement.destination_branch
        )
        db.add(dest_stock)
        db.flush()  # asegura que dest_stock tenga ID

    # Paso 3: Actualizar cantidades
    origin_stock.quantity -= movement.quantity
    dest_stock.quantity += movement.quantity

    # Paso 4: Registrar movimiento
    db_movement = Movement(**movement.model_dump())
    db.add(db_movement)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar el movimiento.")

    db.refresh(db_movement)
    return db_movement

def list_movements(db: Session):
    return db.query(Movement).order_by(Movement.timestamp.desc()).all()
