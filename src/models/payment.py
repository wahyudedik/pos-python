"""
Payment Model
ORM model untuk payment records
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from src.config.database import Base


class Payment(Base):
    """Payment record model"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer)  # Reference to transaction
    
    method = Column(String(50), nullable=False)  # Tunai, GoPay, QRIS, etc
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")  # pending, success, failed
    
    # Untuk online payment
    reference_id = Column(String(100))  # Midtrans transaction ID
    gateway_response = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    def __repr__(self) -> str:
        return f"<Payment {self.method} - {self.amount}>"
