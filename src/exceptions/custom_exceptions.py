"""
Custom Exception Classes
Application-specific exceptions untuk POS system
"""


class POSException(Exception):
    """Base exception class untuk semua POS exceptions"""
    pass


class PaymentException(POSException):
    """Exception untuk payment processing errors"""
    pass


class PaymentGatewayException(PaymentException):
    """Exception untuk payment gateway integration errors"""
    pass


class MidtransException(PaymentGatewayException):
    """Exception untuk Midtrans API errors"""
    pass


class ValidationException(POSException):
    """Exception untuk data validation errors"""
    pass


class InventoryException(POSException):
    """Exception untuk inventory management errors"""
    pass


class InsufficientStockException(InventoryException):
    """Exception ketika stock tidak cukup"""
    pass


class ProductNotFoundException(InventoryException):
    """Exception ketika produk tidak ditemukan"""
    pass


class AuthenticationException(POSException):
    """Exception untuk authentication errors"""
    pass


class AuthorizationException(POSException):
    """Exception untuk authorization/permission errors"""
    pass


class DatabaseException(POSException):
    """Exception untuk database operation errors"""
    pass


class ConnectionException(DatabaseException):
    """Exception untuk database connection errors"""
    pass


class TransactionException(POSException):
    """Exception untuk transaction processing errors"""
    pass


class ReportException(POSException):
    """Exception untuk report generation errors"""
    pass


class ConfigurationException(POSException):
    """Exception untuk configuration errors"""
    pass


class BackupException(POSException):
    """Exception untuk backup/restore operations"""
    pass
