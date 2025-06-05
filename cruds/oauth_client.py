from sqlalchemy.orm import Session
from models.oauth_client import OAuthClient
from utils.auth import verify_password
from fastapi import HTTPException, status

def get_oauth_client_by_client_id(db: Session, client_id: str) -> OAuthClient:
    """Retrieve an OAuth client by client_id."""
    return db.query(OAuthClient).filter(OAuthClient.client_id == client_id).first()

def validate_oauth_client(db: Session, client_id: str, client_secret: str) -> OAuthClient:
    """Validate OAuth client credentials."""
    client = get_oauth_client_by_client_id(db, client_id)
    if not client or not verify_password(client.client_secret, client_secret):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid client credentials")
    return client

def create_oauth_client(db: Session, client_id: str, client_secret: str, name: str) -> OAuthClient:
    """Create a new OAuth client."""
    client = OAuthClient(client_id=client_id, name=name)
    client.set_client_secret(client_secret)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
