"""
Validators
Input validation utilities
"""

import re
from typing import Any, Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.
    
    Args:
        email: Email to validate
    
    Returns:
        Tuple (is_valid, message)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True, "Valid email"
    
    return False, "Invalid email format"


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number (Indonesian).
    
    Args:
        phone: Phone number to validate
    
    Returns:
        Tuple (is_valid, message)
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if starts with 0 or +62
    if cleaned.startswith('+62'):
        cleaned = '0' + cleaned[3:]
    
    # Should be 10-13 digits
    if not re.match(r'^0[0-9]{9,12}$', cleaned):
        return False, "Invalid phone number format"
    
    return True, "Valid phone number"


def validate_number(value: Any) -> Tuple[bool, str]:
    """
    Validate if value is a number.
    
    Args:
        value: Value to validate
    
    Returns:
        Tuple (is_valid, message)
    """
    try:
        float(value)
        return True, "Valid number"
    except (ValueError, TypeError):
        return False, "Invalid number format"


def validate_positive_number(value: Any) -> Tuple[bool, str]:
    """
    Validate if value is positive number.
    
    Args:
        value: Value to validate
    
    Returns:
        Tuple (is_valid, message)
    """
    is_valid, msg = validate_number(value)
    
    if not is_valid:
        return False, msg
    
    if float(value) <= 0:
        return False, "Number must be positive"
    
    return True, "Valid positive number"


def validate_barcode(barcode: str) -> Tuple[bool, str]:
    """
    Validate barcode format.
    
    Args:
        barcode: Barcode to validate
    
    Returns:
        Tuple (is_valid, message)
    """
    barcode = barcode.strip()
    
    if not barcode:
        return False, "Barcode cannot be empty"
    
    if len(barcode) < 5:
        return False, "Barcode too short (minimum 5 characters)"
    
    if len(barcode) > 50:
        return False, "Barcode too long (maximum 50 characters)"
    
    return True, "Valid barcode"


def validate_sku(sku: str) -> Tuple[bool, str]:
    """
    Validate SKU format.
    
    Args:
        sku: SKU to validate
    
    Returns:
        Tuple (is_valid, message)
    """
    # SKU should be alphanumeric with optional hyphens/underscores
    if not re.match(r'^[a-zA-Z0-9_\-]{1,50}$', sku):
        return False, "Invalid SKU format"
    
    return True, "Valid SKU"


def validate_quantity(qty: Any) -> Tuple[bool, str]:
    """
    Validate quantity.
    
    Args:
        qty: Quantity to validate
    
    Returns:
        Tuple (is_valid, message)
    """
    try:
        qty_int = int(qty)
        
        if qty_int <= 0:
            return False, "Quantity must be greater than 0"
        
        if qty_int > 999999:
            return False, "Quantity too large (maximum 999999)"
        
        return True, "Valid quantity"
    
    except (ValueError, TypeError):
        return False, "Invalid quantity format"
