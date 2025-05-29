from sqlalchemy.orm import Session
from models.stock import Stock
from models.product import Product
from models.branch import Branch
from schemas.stock import StockCreate, StockUpdate
from fastapi import HTTPException


def create_stock(db: Session, stock: StockCreate):
    """Create a new stock entry."""
    # Verify product and branch exist
    product = db.query(Product).filter(Product.id == stock.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    branch = db.query(Branch).filter(Branch.id == stock.branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    # Check for existing stock entry
    existing_stock = db.query(Stock).filter_by(product_id=stock.product_id, branch_id=stock.branch_id).first()
    if existing_stock:
        raise HTTPException(status_code=400, detail="Stock entry already exists for this product and branch")

    db_stock = Stock(**stock.model_dump())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def get_stock(db: Session, branch_id: int | None = None):
    """Get stock entries, optionally filtered by branch_id."""
    query = db.query(Stock)
    if branch_id:
        query = query.filter(Stock.branch_id == branch_id)
    return query.all()


def update_stock(db: Session, stock_id: int, stock_data: StockUpdate):
    """Update a stock entry."""
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        return None
    for field, value in stock_data.model_dump(exclude_unset=True).items():
        setattr(stock, field, value)
    db.commit()
    db.refresh(stock)
    return stock


def delete_stock(db: Session, stock_id: int):
    """Delete a stock entry."""
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        return False
    db.delete(stock)
    db.commit()
    return True