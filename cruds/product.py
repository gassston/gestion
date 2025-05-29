from sqlalchemy.orm import Session
from models.product import Product
from models.stock import Stock
from schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException

def get_products(db: Session):
    """Get all products."""
    return db.query(Product).all()

def get_product(db: Session, product_id: int):
    """Get a product by ID."""
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    """Create a new product."""
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product name already exists")
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    """Update a product."""
    product = get_product(db, product_id)
    if not product:
        return None
    update_data = product_data.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"]:
        existing_product = db.query(Product).filter(Product.name == update_data["name"], Product.id != product_id).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="Product name already exists")
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    """Delete a product."""
    product = get_product(db, product_id)
    if not product:
        return False
    # Check for associated stock
    if db.query(Stock).filter(Stock.product_id == product_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete product with associated stock")
    db.delete(product)
    db.commit()
    return True
