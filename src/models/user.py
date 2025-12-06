"""
User Model
ORM model untuk operator/cashier
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from src.config.database import Base
import enum


class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    MANAGER = "manager"
    CASHIER = "cashier"
    OPERATOR = "operator"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255), nullable=False)
    
    full_name = Column(String(255))
    phone = Column(String(20))
    
    role = Column(Enum(UserRole), default=UserRole.OPERATOR)
    is_active = Column(Boolean, default=True)
    
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<User {self.username}>"
