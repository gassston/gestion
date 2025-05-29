from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.base import Base

class Movement(Base):
    __tablename__ = 'movements'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    origin_branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    destination_branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    product = relationship('Product', backref='movements', lazy='select')
    origin_branch = relationship('Branch', foreign_keys=[origin_branch_id], backref='outgoing_movements', lazy='select')
    destination_branch = relationship('Branch', foreign_keys=[destination_branch_id], backref='incoming_movements', lazy='select')
    user = relationship('User', backref='movements', lazy='select')

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('origin_branch_id != destination_branch_id', name='check_different_branches'),
    )

    def __repr__(self):
        return f'<Movement {self.id} for Product {self.product_id}>'