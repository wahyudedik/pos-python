"""
Custom Exception Classes
Application-specific exceptions
"""


class POSException(Exception):
    """Base exception untuk semua POS exceptions"""
    pass


class PaymentException(POSException):
    """Exception untuk payment processing"""
    pass


class ValidationException(POSException):
    """Exception untuk validation errors"""
    pass


class InventoryException(POSException):
    """Exception untuk inventory operations"""
    pass


class InsufficientStockException(InventoryException):
    """Raised when stock is insufficient"""
    pass


class ProductNotFoundException(InventoryException):
    """Raised when product is not found"""
    pass


class AuthenticationException(POSException):
    """Exception untuk authentication"""
    pass


class AuthorizationException(POSException):
    """Exception untuk authorization"""
    pass


class DatabaseException(POSException):
    """Exception untuk database operations"""
    pass


class TransactionException(POSException):
    """Exception untuk transaction operations"""
    pass


class ConfigurationException(POSException):
    """Exception untuk configuration errors"""
    pass
