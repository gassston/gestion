from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.base import Base

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.UTC), onupdate=lambda: datetime.now(timezone.UTC))

    product = relationship('Product', backref='stocks', lazy='select')
    branch = relationship('Branch', backref='stocks', lazy='select')

    __table_args__ = (
        UniqueConstraint('product_id', 'branch_id', name='uix_product_branch'),
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
    )

    def __repr__(self):
        return f'<Stock Product {self.product_id} at Branch {self.branch_id}>'
