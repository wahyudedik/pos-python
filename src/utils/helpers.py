"""
Helper Functions
Utility functions untuk POS system
"""

from typing import Any, List, Dict
from datetime import datetime


def generate_order_id(prefix: str = "ORD") -> str:
    """
    Generate unique order ID.
    
    Args:
        prefix: Prefix untuk order ID
    
    Returns:
        Generated order ID (e.g., ORD-20251204-001)
    """
    from datetime import datetime
    import random
    
    date_str = datetime.now().strftime("%Y%m%d")
    random_num = random.randint(1000, 9999)
    return f"{prefix}-{date_str}-{random_num}"


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks.
    
    Args:
        lst: List to split
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def sanitize_input(value: str) -> str:
    """
    Sanitize user input untuk prevent SQL injection.
    
    Args:
        value: Input value to sanitize
    
    Returns:
        Sanitized value
    """
    if not isinstance(value, str):
        return str(value)
    
    # Remove potentially dangerous characters
    dangerous_chars = [";", "'", '"', "--", "/*", "*/"]
    sanitized = value
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")
    
    return sanitized.strip()


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string ke max length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix when truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def get_time_of_day() -> str:
    """
    Get time of day greeting.
    
    Returns:
        Time-based greeting (Pagi, Siang, Sore, Malam)
    """
    hour = datetime.now().hour
    
    if 5 <= hour < 11:
        return "Pagi"
    elif 11 <= hour < 15:
        return "Siang"
    elif 15 <= hour < 18:
        return "Sore"
    else:
        return "Malam"
