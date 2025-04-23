from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.base import get_db
from models.stock import Stock
from schemas.stock import StockCreate, StockResponse, StockUpdate
from cruds import stock

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.get("", response_model=list[StockResponse])
def list_stock(db: Session = Depends(get_db)):
    stock_entries = db.query(Stock).options(joinedload(Stock.product)).all()
    return stock_entries

@router.get("", response_model=List[StockResponse])
def get_stock(branch: str = None, db: Session = Depends(get_db)):
    return stock.get_stock(db, branch)

@router.put("/{stock_id}", response_model=StockResponse)
def update_stock(stock_id: int, updated_stock: StockUpdate, db: Session = Depends(get_db)):
    updated = stock.update_stock(db, stock_id, updated_stock)
    if not updated:
        raise HTTPException(status_code=404, detail="Stock ID not found")
    return updated

@router.post("", response_model=StockResponse)
def create_stock(new_stock: StockCreate, db: Session = Depends(get_db)):
    return stock.create_stock(db, new_stock)

@router.delete("/{stock_id}")
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    deleted = stock.delete_stock(db, stock_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Stock ID not found")
    return {"message": "Stock ID deleted"}