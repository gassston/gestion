from sqlalchemy import Column, Integer, String, DateTime
from db.base import Base
from datetime import datetime

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    origin_branch = Column(String, nullable=False)
    destination_branch = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)