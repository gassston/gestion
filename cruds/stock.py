from sqlalchemy.orm import Session
from models.stock import Stock
from schemas.stock import StockCreate, StockUpdate

def create_stock(db: Session, stock: StockCreate):
    db_stock = Stock(**stock.model_dump(exclude_unset=True))
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stock(db: Session, branch: str = None):
    query = db.query(Stock)
    if branch:
        query = query.filter(Stock.branch == branch)
    return query.all()

def update_stock(db: Session, stock_id: int, stock_data: StockUpdate):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        return None
    for field, value in stock_data.model_dump(exclude_unset=True).items():
        setattr(stock, field, value)
    db.commit()
    db.refresh(stock)
    return stock

def delete_stock(db: Session, stock_id: int):
    stock = db.query(Stock).get(stock_id)
    if not stock:
        return {"error": "Stock not found"}
    db.delete(stock)
    db.commit()
    return {"message": "Stock deleted"}