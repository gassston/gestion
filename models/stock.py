from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product")
    branch = relationship("Branch")
