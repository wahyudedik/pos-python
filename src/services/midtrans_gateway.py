"""
Midtrans Payment Gateway Integration
Wrapper untuk Midtrans API
"""

import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class MidtransGateway:
    """Midtrans API Gateway Wrapper"""

    def __init__(self, server_key: str, environment: str = "sandbox"):
        """
        Initialize Midtrans gateway.
        
        Args:
            server_key: Midtrans server key
            environment: sandbox atau production
        """
        self.server_key = server_key
        self.environment = environment
        self.api_url = (
            "https://api.midtrans.com"
            if environment == "production"
            else "https://api.sandbox.midtrans.com"
        )
        self.timeout = 30

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers untuk Midtrans API requests"""
        import base64
        credentials = f"{self.server_key}:"
        encoded = base64.b64encode(credentials.encode()).decode()
        
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded}",
        }

    def create_transaction(
        self,
        order_id: str,
        gross_amount: int,
        customer_email: str,
        customer_phone: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create transaction di Midtrans.
        
        Args:
            order_id: Order ID
            gross_amount: Total amount
            customer_email: Customer email
            customer_phone: Customer phone
            **kwargs: Additional parameters
        
        Returns:
            Transaction response
        """
        try:
            payload = {
                "transaction_details": {
                    "order_id": order_id,
                    "gross_amount": gross_amount,
                },
                "customer_details": {
                    "email": customer_email,
                    "phone": customer_phone,
                },
            }
            payload.update(kwargs)

            response = requests.post(
                f"{self.api_url}/charge",
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout,
            )

            if response.status_code not in [200, 201]:
                raise Exception(f"Midtrans API error: {response.text}")

            logger.info(f"Transaction created: {order_id}")
            return response.json()

        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise

    def get_transaction_status(self, order_id: str) -> Dict[str, Any]:
        """
        Get transaction status.
        
        Args:
            order_id: Order ID
        
        Returns:
            Transaction status
        """
        try:
            response = requests.get(
                f"{self.api_url}/{order_id}/status",
                headers=self._get_headers(),
                timeout=self.timeout,
            )

            if response.status_code != 200:
                raise Exception(f"Midtrans API error: {response.text}")

            return response.json()

        except Exception as e:
            logger.error(f"Error getting transaction status: {e}")
            raise
