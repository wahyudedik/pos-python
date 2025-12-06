"""
Currency Utilities
Formatting dan parsing untuk currency operations
"""

from typing import Union


def format_currency(amount: Union[int, float], currency: str = "IDR") -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Amount to format
        currency: Currency code (default: IDR)
    
    Returns:
        Formatted currency string (e.g., "Rp 1.234.567,89")
    """
    if currency == "IDR":
        # Indonesian Rupiah formatting
        if isinstance(amount, float):
            amount = int(amount)
        
        # Format dengan titik sebagai separator ribuan
        formatted = f"{amount:,}".replace(",", ".")
        return f"Rp {formatted}"
    
    elif currency == "USD":
        return f"${amount:,.2f}"
    
    else:
        return f"{currency} {amount:,.2f}"


def parse_currency(currency_str: str) -> float:
    """
    Parse currency string to float amount.
    
    Args:
        currency_str: Currency string (e.g., "Rp 1.234.567,89" atau "1234567.89")
    
    Returns:
        Float amount
    """
    # Remove currency prefix
    cleaned = currency_str.replace("Rp", "").replace("$", "").strip()
    
    # Remove formatting
    if "," in cleaned and "." in cleaned:
        # IDR format: 1.234.567,89
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "," in cleaned:
        # Ambiguous - assume comma is decimal separator
        cleaned = cleaned.replace(",", ".")
    
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def round_to_nearest_denomination(amount: float, denomination: int = 100) -> int:
    """
    Round amount to nearest denomination (untuk pembulatan kembalian).
    
    Args:
        amount: Amount to round
        denomination: Denomination to round to (default: 100)
    
    Returns:
        Rounded amount
    """
    return round(amount / denomination) * denomination


def calculate_change(total: float, amount_paid: float, denomination: int = 100) -> dict:
    """
    Calculate change and round to nearest denomination.
    
    Args:
        total: Total amount
        amount_paid: Amount paid by customer
        denomination: Denomination for rounding (default: 100)
    
    Returns:
        Dictionary dengan:
            - exact_change: Exact change amount
            - rounded_change: Rounded change amount
            - excess: Kelebihan pembulatan
    """
    exact_change = amount_paid - total
    rounded_change = round_to_nearest_denomination(exact_change, denomination)
    excess = rounded_change - exact_change
    
    return {
        'exact_change': exact_change,
        'rounded_change': rounded_change,
        'excess': excess,
    }
