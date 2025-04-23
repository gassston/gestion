from sqlalchemy.orm import Session
from models.client import Client
from schemas.client import ClientCreate

def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session):
    return db.query(Client).all()

def update_client(db: Session, client_id: int, client_data: ClientCreate):
    client = db.query(Client).get(client_id)
    if not client:
        return None
    for field, value in client_data.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: int):
    client = db.query(Client).get(client_id)
    if not client:
        return {"error": "Client not found"}
    db.delete(client)
    db.commit()
    return {"message": "Client deleted"}