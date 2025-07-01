from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy
from db.base import get_db
from schemas.product import ProductResponse, ProductCreate, ProductUpdate
from cruds.product import get_wine, get_wines, create_wine, update_wine, delete_wine
from utils.auth import get_current_admin
from utils.logger import get_logger
from utils.pagination import CustomCursorParams

logger = get_logger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=CursorPage[ProductResponse])
def read_wines(
    db: Session = Depends(get_db),
    name: str | None = None,
    region: str | None = None,
    vintage: int | None = None,
    sort: str = "id_asc",  # Change default to id_asc for cursor compatibility
    params: CustomCursorParams = Depends()
):
    """
    Get products with cursor-based pagination, optionally filtered by name, region, or vintage.

    Args:
        db: Database session.
        name: Optional filter by product name (partial match).
        region: Optional filter by product region.
        vintage: Optional filter by product vintage year.
        sort: Sort order (e.g., 'id_asc', 'id_desc', 'name_asc', 'name_desc', 'vintage_asc', 'vintage_desc').
        params: Cursor pagination parameters (cursor and size).
    """
    valid_sorts = ["id_asc", "id_desc", "name_asc", "name_desc", "vintage_asc", "vintage_desc"]
    if sort not in valid_sorts:
        raise HTTPException(status_code=400, detail=f"Invalid sort parameter. Must be one of: {', '.join(valid_sorts)}")
    logger.info(f"Fetching products with filters: name={name}, region={region}, vintage={vintage}, sort={sort}, cursor={params.cursor}, size={params.size}")
    try:
        query = get_wines(db, name=name, region=region, vintage=vintage, sort=sort)
        return paginate_sqlalchemy(query, params)
    except ValueError as e:
        logger.error(f"Invalid sort parameter: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching products")

@router.get("/{wine_id}", response_model=ProductResponse)
def read_wine(wine_id: int, db: Session = Depends(get_db)):
    """Get a product by ID."""
    logger.info(f"Fetching product ID={wine_id}")
    db_wine = get_wine(db, wine_id=wine_id)
    if db_wine is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_wine

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin)])
def create_new_wine(wine: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product (admin only)."""
    logger.info(f"Creating product: {wine.name}")
    return create_wine(db, wine)

@router.put("/{wine_id}", response_model=ProductResponse, dependencies=[Depends(get_current_admin)])
def update_existing_wine(wine_id: int, wine: ProductUpdate, db: Session = Depends(get_db)):
    """Update a product (admin only)."""
    logger.info(f"Updating product ID={wine_id}")
    db_wine = update_wine(db, wine_id, wine)
    if db_wine is None:
        raise HTTPException(status_code=404, detail=" product's not found")
    return db_wine

@router.delete("/{wine_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
def delete_existing_wine(wine_id: int, db: Session = Depends(get_db)):
    """Delete a product (admin only)."""
    logger.info(f"Deleting product ID={wine_id}")
    success = delete_wine(db, wine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
