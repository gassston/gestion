from sqlalchemy import Column, Integer, String
from db.base import Base
from utils.auth import hash_password

class OAuthClient(Base):
    __tablename__ = "oauth_clients"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True, nullable=False)
    client_secret = Column(String, nullable=False)
    name = Column(String, nullable=False)

    def set_client_secret(self, secret: str):
        """Hash and set the client secret."""
        self.client_secret = hash_password(secret)
