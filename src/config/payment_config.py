"""
Payment Gateway Configuration
Midtrans integration setup & configuration
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class PaymentConfig:
    """Payment Gateway Configuration Manager"""

    # ===== MIDTRANS CONFIGURATION =====
    MIDTRANS_ENABLED: bool = os.getenv("MIDTRANS_ENABLED", "True").lower() == "true"
    MIDTRANS_ENVIRONMENT: str = os.getenv("MIDTRANS_ENVIRONMENT", "sandbox")
    MIDTRANS_SERVER_KEY: str = os.getenv("MIDTRANS_SERVER_KEY", "")
    MIDTRANS_CLIENT_KEY: str = os.getenv("MIDTRANS_CLIENT_KEY", "")
    MIDTRANS_MERCHANT_ID: str = os.getenv("MIDTRANS_MERCHANT_ID", "")

    # API Endpoint
    MIDTRANS_API_BASE_URL: str = (
        "https://api.midtrans.com"
        if MIDTRANS_ENVIRONMENT == "production"
        else "https://api.sandbox.midtrans.com"
    )

    # ===== PAYMENT METHODS CONFIGURATION =====
    PAYMENT_METHODS: Dict[str, Dict[str, Any]] = {
        "cash": {
            "name": "Tunai",
            "code": "cash",
            "enabled": True,
            "requires_gateway": False,
            "display_order": 1,
        },
        "bank_transfer": {
            "name": "Transfer Bank",
            "code": "bank_transfer",
            "enabled": True,
            "requires_gateway": True,
            "gateway": "midtrans",
            "display_order": 2,
        },
        "qris": {
            "name": "QRIS",
            "code": "qris",
            "enabled": True,
            "requires_gateway": True,
            "gateway": "midtrans",
            "display_order": 3,
        },
        "gopay": {
            "name": "GoPay",
            "code": "gopay",
            "enabled": True,
            "requires_gateway": True,
            "gateway": "midtrans",
            "display_order": 4,
        },
        "ovo": {
            "name": "OVO",
            "code": "ovo",
            "enabled": True,
            "requires_gateway": True,
            "gateway": "midtrans",
            "display_order": 5,
        },
        "dana": {
            "name": "DANA",
            "code": "dana",
            "enabled": True,
            "requires_gateway": True,
            "gateway": "midtrans",
            "display_order": 6,
        },
        "shopeepay": {
            "name": "ShopeePay",
            "code": "shopeepay",
            "enabled": True,
            "requires_gateway": True,
            "gateway": "midtrans",
            "display_order": 7,
        },
        "credit_card": {
            "name": "Kartu Kredit",
            "code": "credit_card",
            "enabled": True,
            "requires_gateway": True,
            "gateway": "midtrans",
            "display_order": 8,
        },
        "debit_card": {
            "name": "Kartu Debit",
            "code": "debit_card",
            "enabled": True,
            "requires_gateway": True,
            "gateway": "midtrans",
            "display_order": 9,
        },
    }

    PAYMENT_GATEWAY_TIMEOUT: int = 30  # seconds
    PAYMENT_GATEWAY_RETRY_ATTEMPTS: int = 3
    TRANSACTION_TIMEOUT: int = 900  # 15 minutes

    @classmethod
    def get_payment_method(cls, code: str) -> Optional[Dict[str, Any]]:
        """Get payment method configuration by code."""
        return cls.PAYMENT_METHODS.get(code)

    @classmethod
    def get_enabled_payment_methods(cls) -> Dict[str, Dict[str, Any]]:
        """Get all enabled payment methods."""
        return {
            code: config
            for code, config in cls.PAYMENT_METHODS.items()
            if config.get("enabled", True)
        }

    @classmethod
    def validate_midtrans_config(cls) -> bool:
        """Validate Midtrans configuration."""
        if not cls.MIDTRANS_ENABLED:
            return True

        if not cls.MIDTRANS_SERVER_KEY or not cls.MIDTRANS_CLIENT_KEY:
            raise ValueError(
                "Midtrans credentials tidak ditemukan. "
                "Pastikan MIDTRANS_SERVER_KEY dan MIDTRANS_CLIENT_KEY di-set di .env"
            )

        return True

    @classmethod
    def get_midtrans_config(cls) -> Dict[str, Any]:
        """Get complete Midtrans configuration."""
        cls.validate_midtrans_config()
        
        return {
            "enabled": cls.MIDTRANS_ENABLED,
            "environment": cls.MIDTRANS_ENVIRONMENT,
            "server_key": cls.MIDTRANS_SERVER_KEY,
            "client_key": cls.MIDTRANS_CLIENT_KEY,
            "merchant_id": cls.MIDTRANS_MERCHANT_ID,
            "api_base_url": cls.MIDTRANS_API_BASE_URL,
        }
