"""
Transaction Model
ORM model untuk penjualan/transaksi
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from src.config.database import Base
import enum


class TransactionStatus(str, enum.Enum):
    """Status transaksi"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Transaction(Base):
    """Transaction/Sales model"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    order_id = Column(String(50), unique=True, nullable=False, index=True)
    cashier_id = Column(Integer)  # Reference to user
    customer_id = Column(Integer)  # Optional - for customer tracking
    
    subtotal = Column(Float, nullable=False)
    discount = Column(Float, default=0)
    tax = Column(Float, default=0)
    total = Column(Float, nullable=False)
    
    payment_method = Column(String(50), nullable=False)  # Tunai, GoPay, QRIS, dll
    payment_status = Column(String(50), default="pending")
    
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    
    notes = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Transaction {self.order_id}>"
