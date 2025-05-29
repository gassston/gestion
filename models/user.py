from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from db.base import Base
import enum

# Define Role Enum for PostgreSQL
class Role(enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(Role), default=Role.user, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(pwhash=self.hashed_password, password=password)

    def __repr__(self):
        return f'<User {self.username}>'