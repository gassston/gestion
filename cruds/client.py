from sqlalchemy.orm import Session
from models.client import Client
from schemas.client import ClientCreate, ClientUpdate
from fastapi import HTTPException

def create_client(db: Session, client: ClientCreate):
    """Create a new client."""
    if db.query(Client).filter(Client.email == client.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    db_client = Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session):
    """Get all clients."""
    return db.query(Client).all()

def update_client(db: Session, client_id: int, client_data: ClientUpdate):
    """Update a client."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None
    update_data = client_data.model_dump(exclude_unset=True)
    if "email" in update_data and update_data["email"]:
        existing_client = db.query(Client).filter(Client.email == update_data["email"], Client.id != client_id).first()
        if existing_client:
            raise HTTPException(status_code=400, detail="Email already exists")
    for key, value in update_data.items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: int):
    """Delete a client."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return False
    db.delete(client)
    db.commit()
    return True