from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from fastapi_pagination import Page, paginate
from db.base import get_db
from models.stock import Stock
from schemas.stock import StockCreate, StockUpdate, StockResponse
from cruds import stock
from utils.auth import get_current_admin
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.get("", response_model=Page[StockResponse])
def list_stock(branch_id: int | None = None, db: Session = Depends(get_db)):
    """Get stock entries, optionally filtered by branch_id, with pagination."""
    stock_entries = db.query(Stock).options(joinedload(Stock.product))
    if branch_id:
        stock_entries = stock_entries.filter(Stock.branch_id == branch_id)
    return paginate(stock_entries.all())

@router.post("", response_model=StockResponse, status_code=201, dependencies=[Depends(get_current_admin)])
def create_stock(new_stock: StockCreate, db: Session = Depends(get_db)):
    """Create a new stock entry (admin only)."""
    logger.info(f"Creating stock for product ID: {new_stock.product_id} at branch ID: {new_stock.branch_id}")
    return stock.create_stock(db, new_stock)

@router.put("/{stock_id}", response_model=StockResponse, dependencies=[Depends(get_current_admin)])
def update_stock(stock_id: int, updated_stock: StockUpdate, db: Session = Depends(get_db)):
    """Update a stock entry (admin only)."""
    updated = stock.update_stock(db, stock_id, updated_stock)
    if not updated:
        raise HTTPException(status_code=404, detail="Stock ID not found")
    logger.info(f"Updated stock ID: {stock_id}")
    return updated

@router.delete("/{stock_id}", dependencies=[Depends(get_current_admin)])
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    """Delete a stock entry (admin only)."""
    deleted = stock.delete_stock(db, stock_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Stock ID not found")
    logger.info(f"Deleted stock ID: {stock_id}")
    return {"message": "Stock ID deleted"}