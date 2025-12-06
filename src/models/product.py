"""
Product Model
ORM model untuk produk
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from src.config.database import Base


class Product(Base):
    """Product model"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    category = Column(String(100))
    cost_price = Column(Float, nullable=False)  # Harga beli
    selling_price = Column(Float, nullable=False)  # Harga jual
    quantity = Column(Integer, default=0)  # Current stock
    min_quantity = Column(Integer, default=10)  # Reorder point
    barcode = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Product {self.sku} - {self.name}>"
