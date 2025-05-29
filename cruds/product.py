from sqlalchemy.orm import Session
from models.product import Product
from models.stock import Stock
from schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException


def get_wines(
        db: Session,
        name: str = None,
        region: str = None,
        vintage: int = None,
        sort: str = "name_asc",
        cursor: int = None,
        limit: int = 100
):
    """Get wines with filtering, sorting, and cursor-based pagination."""
    query = db.query(Product)

    # Apply filters
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if region:
        query = query.filter(Product.region.ilike(f"%{region}%"))
    if vintage is not None:
        query = query.filter(Product.vintage == vintage)

    # Get total count
    total = query.count()

    # Apply sorting
    if sort == "name_asc":
        query = query.order_by(Product.name.asc())
    elif sort == "name_desc":
        query = query.order_by(Product.name.desc())
    elif sort == "vintage_asc":
        query = query.order_by(Product.vintage.asc())
    elif sort == "vintage_desc":
        query = query.order_by(Product.vintage.desc())
    else:
        raise HTTPException(status_code=400, detail="Invalid sort parameter")

    # Apply cursor-based pagination
    if cursor:
        query = query.filter(Product.id > cursor)

    # Limit results
    wines = query.limit(limit).all()

    # Determine next cursor
    next_cursor = wines[-1].id if wines and len(wines) == limit else None

    return {"items": wines, "total": total, "next_cursor": next_cursor}


def get_wine(db: Session, wine_id: int):
    """Get a wine by ID."""
    return db.query(Product).filter(Product.id == wine_id).first()


def create_wine(db: Session, wine: ProductCreate):
    """Create a new wine."""
    existing_wine = db.query(Product).filter(Product.name == wine.name).first()
    if existing_wine:
        raise HTTPException(status_code=400, detail="Wine name already exists")
    db_wine = Product(**wine.model_dump())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    return db_wine


def update_wine(db: Session, wine_id: int, wine_data: ProductUpdate):
    """Update a wine."""
    wine = get_wine(db, wine_id)
    if not wine:
        return None
    update_data = wine_data.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"]:
        existing_wine = db.query(Product).filter(Product.name == update_data["name"], Product.id != wine_id).first()
        if existing_wine:
            raise HTTPException(status_code=400, detail="Wine name already exists")
    for key, value in update_data.items():
        setattr(wine, key, value)
    db.commit()
    db.refresh(wine)
    return wine


def delete_wine(db: Session, wine_id: int):
    """Delete a wine."""
    wine = get_wine(db, wine_id)
    if not wine:
        return False
    # Check for associated stock
    if db.query(Stock).filter(Stock.product_id == wine_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete wine with associated stock")
    db.delete(wine)
    db.commit()
    return True