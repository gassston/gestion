from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from db.base import Base

class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Branch {self.name}>'
