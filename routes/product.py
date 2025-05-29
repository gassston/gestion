from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.base import get_db
from schemas.product import ProductResponse, ProductCreate, ProductUpdate, ProductListResponse
from cruds.product import get_wine, get_wines, create_wine, update_wine, delete_wine
from utils.auth import get_current_admin

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=ProductListResponse)
def read_wines(
    db: Session = Depends(get_db),
    name: str = None,
    region: str = None,
    vintage: int = None,
    sort: str = "name_asc",
    cursor: int = None,
    limit: int = 100
):
    return get_wines(db, name=name, region=region, vintage=vintage, sort=sort, cursor=cursor, limit=limit)

@router.get("/{wine_id}", response_model=ProductResponse)
def read_wine(wine_id: int, db: Session = Depends(get_db)):
    db_wine = get_wine(db, wine_id=wine_id)
    if db_wine is None:
        raise HTTPException(status_code=404, detail="Wine not found")
    return db_wine

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin)])
def create_new_wine(wine: ProductCreate, db: Session = Depends(get_db)):
    return create_wine(db, wine)

@router.put("/{wine_id}", response_model=ProductResponse, dependencies=[Depends(get_current_admin)])
def update_existing_wine(wine_id: int, wine: ProductUpdate, db: Session = Depends(get_db)):
    db_wine = update_wine(db, wine_id, wine)
    if db_wine is None:
        raise HTTPException(status_code=404, detail="Wine not found")
    return db_wine

@router.delete("/{wine_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
def delete_existing_wine(wine_id: int, db: Session = Depends(get_db)):
    success = delete_wine(db, wine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Wine not found")
    return None