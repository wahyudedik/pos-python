"""
Inventory Model
ORM model untuk inventory tracking
"""

from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.sql import func
from src.config.database import Base


class Inventory(Base):
    """Inventory tracking model"""
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)  # Reference to product
    
    quantity = Column(Integer, default=0)  # Current stock
    min_quantity = Column(Integer, default=10)  # Reorder point
    max_quantity = Column(Integer)  # Optional - max stock
    
    # Tracking
    reason = Column(String(100))  # sale, purchase, adjustment, damage, etc
    notes = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Inventory product_id={self.product_id}, qty={self.quantity}>"
