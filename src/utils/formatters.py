"""
Formatters
Data formatting utilities
"""

from typing import Any, Dict, List
from datetime import datetime


def format_datetime(dt: datetime, format_str: str = "%d/%m/%Y %H:%M:%S") -> str:
    """
    Format datetime object.
    
    Args:
        dt: Datetime object
        format_str: Format string
    
    Returns:
        Formatted datetime string
    """
    if not isinstance(dt, datetime):
        return str(dt)
    
    return dt.strftime(format_str)


def format_date(dt: datetime, format_str: str = "%d/%m/%Y") -> str:
    """Format date only"""
    if not isinstance(dt, datetime):
        return str(dt)
    
    return dt.strftime(format_str)


def format_time(dt: datetime, format_str: str = "%H:%M:%S") -> str:
    """Format time only"""
    if not isinstance(dt, datetime):
        return str(dt)
    
    return dt.strftime(format_str)


def format_quantity(qty: int, unit: str = "") -> str:
    """
    Format quantity dengan unit.
    
    Args:
        qty: Quantity
        unit: Unit (e.g., "pcs", "box", "kg")
    
    Returns:
        Formatted quantity string
    """
    if unit:
        return f"{qty} {unit}"
    return str(qty)


def format_percent(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage.
    
    Args:
        value: Value (0-1 or 0-100)
        decimals: Decimal places
    
    Returns:
        Formatted percentage string
    """
    if value <= 1:
        value = value * 100
    
    return f"{value:.{decimals}f}%"


def format_table_data(data: List[Dict[str, Any]], column_widths: List[int] = None) -> str:
    """
    Format data as text table.
    
    Args:
        data: List of dictionaries
        column_widths: Width for each column
    
    Returns:
        Formatted table string
    """
    if not data:
        return "No data"
    
    keys = list(data[0].keys())
    
    if not column_widths:
        column_widths = [max(len(str(key)), max(len(str(row.get(key, ""))) for row in data)) + 2 for key in keys]
    
    # Header
    header = " ".join(str(key).ljust(width) for key, width in zip(keys, column_widths))
    separator = "-" * len(header)
    
    # Rows
    rows = [header, separator]
    for row in data:
        row_str = " ".join(str(row.get(key, "")).ljust(width) for key, width in zip(keys, column_widths))
        rows.append(row_str)
    
    return "\n".join(rows)
