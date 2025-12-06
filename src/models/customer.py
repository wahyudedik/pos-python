"""
Customer Model
ORM model untuk customer
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from src.config.database import Base


class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    address = Column(String(500))
    
    customer_type = Column(String(50), default="retail")  # retail atau wholesale
    
    loyalty_points = Column(Float, default=0)
    total_purchase = Column(Float, default=0)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Customer {self.name}>"
