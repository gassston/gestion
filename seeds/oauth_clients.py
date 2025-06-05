from sqlalchemy.orm import Session
from cruds.oauth_client import create_oauth_client
from models.oauth_client import OAuthClient
from utils.logger import get_logger

logger = get_logger(__name__)

def seed_oauth_client(db: Session):
    """Seed an initial OAuth client if it doesn't exist."""
    if not db.query(OAuthClient).filter(OAuthClient.client_id == "app123").first():
        create_oauth_client(db, client_id="app123", client_secret="secret456", name="Default OAuth Client")
        logger.info("Seeded default OAuth client")
