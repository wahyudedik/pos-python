"""
Hardware Exception Classes
Custom exceptions for barcode scanner and thermal printer operations
"""


class HardwareException(Exception):
    """Base exception for hardware operations"""
    pass


class ScannerException(HardwareException):
    """Base exception for scanner operations"""
    pass


class ScannerNotConnectedException(ScannerException):
    """Raised when scanner is not connected"""
    pass


class ScannerDisconnectedException(ScannerException):
    """Raised when scanner gets disconnected during operation"""
    pass


class ScannerReadException(ScannerException):
    """Raised when error occurs reading from scanner"""
    pass


class PrinterException(HardwareException):
    """Base exception for printer operations"""
    pass


class PrinterNotConnectedException(PrinterException):
    """Raised when printer is not connected"""
    pass


class PrinterOfflineException(PrinterException):
    """Raised when printer is offline"""
    pass


class PrinterPrintException(PrinterException):
    """Raised when print operation fails"""
    pass
