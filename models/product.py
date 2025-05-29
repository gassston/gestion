from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from db.base import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    vintage = Column(Integer, nullable=True)
    region = Column(String(100), nullable=True)
    grape_variety = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Wine {self.name}>'