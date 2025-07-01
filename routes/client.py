from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy
from fastapi_pagination.cursor import CursorPage
from db.base import get_db
from schemas.client import ClientCreate, ClientUpdate, ClientResponse
from cruds import client
from utils.logger import get_logger
from utils.pagination import CustomCursorParams

logger = get_logger(__name__)

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("", response_model=CursorPage[ClientResponse])
def get_clients(db: Session = Depends(get_db), params: CustomCursorParams = Depends()):
    """Get all clients with cursor-based pagination."""
    logger.info(f"Fetching clients with cursor={params.cursor}, size={params.size}, order={params.order}")
    query = client.get_clients(db)
    return paginate_sqlalchemy(query, params)

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, updated_client: ClientUpdate, db: Session = Depends(get_db)):
    """Update a client."""
    updated = client.update_client(db, client_id, updated_client)
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    logger.info(f"Updated client ID: {client_id}")
    return updated

@router.post("", response_model=ClientResponse, status_code=201)
def create_client(new_client: ClientCreate, db: Session = Depends(get_db)):
    """Create a new client."""
    logger.info(f"Creating client: {new_client.email}")
    return client.create_client(db, new_client)

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Delete a client."""
    deleted = client.delete_client(db, client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")
    logger.info(f"Deleted client ID: {client_id}")
    return {"message": "Client deleted"}