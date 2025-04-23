from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from schemas.client import ClientCreate, ClientResponse
from cruds import client

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return client.get_clients(db)

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, updated_client: ClientCreate, db: Session = Depends(get_db)):
    updated = client.update_client(db, client_id, updated_client)
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated

@router.post("", response_model=ClientResponse)
def create_client(new_client: ClientCreate, db: Session = Depends(get_db)):
    return client.create_client(db, new_client)

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    deleted = client.delete_client(db, client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted"}