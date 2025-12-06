"""
Thermal Printer Service for offline POS system
Handles receipt printing with Epson/Star printer support via ESCPOS protocol
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Tuple
from datetime import datetime

try:
    from escpos.printer import Usb, Network, Serial
    from escpos.exceptions import USBNotFoundError
    HAS_ESCPOS = True
except ImportError:
    HAS_ESCPOS = False

from src.exceptions.hardware_exceptions import (
    PrinterException,
    PrinterNotConnectedException,
    PrinterOfflineException,
    PrinterPrintException
)
from src.utils.currency import format_currency


logger = logging.getLogger(__name__)


class PrinterConnection(Enum):
    """Printer connection type"""
    USB = "usb"
    NETWORK = "network"
    SERIAL = "serial"


@dataclass
class PrinterConfig:
    """Thermal printer configuration"""
    model: str  # epson, star, etc
    connection_type: PrinterConnection
    vendor_id: Optional[int] = None  # For USB
    product_id: Optional[int] = None  # For USB
    ip_address: Optional[str] = None  # For Network
    port: Optional[int] = None  # For Serial/Network (9100 for network printers)
    timeout: int = 10
    receipt_width: int = 80  # Characters, typically 32, 40, or 80


class ThermalPrinterDevice:
    """Represents a thermal printer device with ESCPOS support"""
    
    def __init__(self, config: PrinterConfig):
        """
        Initialize printer device
        
        Args:
            config: PrinterConfig instance
        """
        self.config = config
        self.printer = None
        self.is_connected = False
        
        if not HAS_ESCPOS:
            raise PrinterException("escpos library required")
    
    def connect(self) -> bool:
        """
        Connect to printer
        
        Returns:
            True if connection successful
            
        Raises:
            PrinterNotConnectedException: If connection fails
        """
        try:
            if self.config.connection_type == PrinterConnection.USB:
                self.printer = Usb(
                    self.config.vendor_id,
                    self.config.product_id,
                    timeout=self.config.timeout
                )
            
            elif self.config.connection_type == PrinterConnection.NETWORK:
                self.printer = Network(
                    host=self.config.ip_address,
                    port=self.config.port or 9100,
                    timeout=self.config.timeout
                )
            
            elif self.config.connection_type == PrinterConnection.SERIAL:
                self.printer = Serial(
                    devfile=self.config.ip_address,  # Device path on serial
                    baudrate=9600,
                    timeout=self.config.timeout
                )
            
            self.is_connected = True
            logger.info(f"Printer {self.config.model} connected via {self.config.connection_type.value}")
            return True
            
        except Exception as e:
            self.is_connected = False
            raise PrinterNotConnectedException(f"Failed to connect: {e}")
    
    def print_text(self, text: str, align: str = "left", **kwargs):
        """
        Print text
        
        Args:
            text: Text to print
            align: left, center, right
            **kwargs: Additional escpos parameters
        """
        if not self.is_connected:
            raise PrinterOfflineException("Printer not connected")
        
        try:
            align_code = {"left": "l", "center": "c", "right": "r"}.get(align, "l")
            self.printer.text(text + "\n")
        except Exception as e:
            raise PrinterPrintException(f"Print error: {e}")
    
    def cut_paper(self, mode: str = "full"):
        """
        Cut paper
        
        Args:
            mode: full or partial
        """
        if not self.is_connected:
            raise PrinterOfflineException("Printer not connected")
        
        try:
            if mode == "full":
                self.printer.cut(mode='FULL')
            else:
                self.printer.cut(mode='PART')
        except Exception as e:
            logger.error(f"Cut error: {e}")
    
    def open_drawer(self):
        """Open cash drawer"""
        if not self.is_connected:
            raise PrinterOfflineException("Printer not connected")
        
        try:
            # ESC/POS code to open drawer
            self.printer._raw(b'\x1B\x70\x00\x19\xFA')
        except Exception as e:
            logger.error(f"Drawer open error: {e}")
    
    def disconnect(self):
        """Close printer connection"""
        try:
            if self.printer:
                self.printer.close()
            self.is_connected = False
            logger.info(f"Printer {self.config.model} disconnected")
        except Exception as e:
            logger.warning(f"Disconnect error: {e}")


class ReceiptFormatter:
    """Formats receipt data for thermal printer"""
    
    def __init__(self, width: int = 32):
        """
        Initialize formatter
        
        Args:
            width: Receipt width in characters (32, 40, or 80)
        """
        self.width = width
    
    def center_text(self, text: str) -> str:
        """Center text on receipt"""
        if len(text) >= self.width:
            return text[:self.width]
        padding = (self.width - len(text)) // 2
        return " " * padding + text
    
    def left_right_text(self, left: str, right: str) -> str:
        """Format text with left and right alignment"""
        available = self.width - len(left) - len(right)
        if available < 0:
            # Truncate if necessary
            right = right[:self.width - len(left)]
            available = 0
        return left + " " * available + right
    
    def line_separator(self, char: str = "-") -> str:
        """Create separator line"""
        return char * self.width
    
    def format_receipt_header(self, store_name: str, address: str = "", time: datetime = None) -> List[str]:
        """Format receipt header"""
        if time is None:
            time = datetime.now()
        
        lines = [
            self.center_text(store_name),
            "",
        ]
        if address:
            lines.append(self.center_text(address))
        
        lines.extend([
            self.line_separator(),
            self.center_text(f"{time.strftime('%d/%m/%Y %H:%M:%S')}"),
            self.line_separator(),
            ""
        ])
        return lines
    
    def format_receipt_items(self, items: List[Dict]) -> List[str]:
        """
        Format receipt items table
        
        Args:
            items: List of dicts with keys: name, qty, price, total
        """
        lines = []
        for item in items:
            name = item.get('name', '')[:self.width - 12]
            qty = str(item.get('qty', 1))
            price = format_currency(item.get('price', 0), currency='IDR')
            total = format_currency(item.get('total', 0), currency='IDR')
            
            lines.append(name)
            lines.append(self.left_right_text(f"{qty}x", f"{total}"))
            lines.append("")
        
        return lines
    
    def format_receipt_totals(self, subtotal: float, discount: float = 0, 
                            tax: float = 0, total: float = 0) -> List[str]:
        """Format totals section"""
        lines = [
            self.line_separator(),
            self.left_right_text(
                "Subtotal",
                format_currency(subtotal, currency='IDR')
            ),
        ]
        
        if discount > 0:
            lines.append(self.left_right_text(
                "Discount",
                f"-{format_currency(discount, currency='IDR')}"
            ))
        
        if tax > 0:
            lines.append(self.left_right_text(
                "Tax",
                format_currency(tax, currency='IDR')
            ))
        
        lines.extend([
            self.line_separator(),
            self.left_right_text(
                "TOTAL",
                format_currency(total, currency='IDR')
            ),
            ""
        ])
        
        return lines
    
    def format_receipt_payment(self, payment_method: str, cash_amount: float = None,
                             change: float = None) -> List[str]:
        """Format payment section"""
        lines = [
            f"Payment: {payment_method}",
        ]
        
        if cash_amount:
            lines.append(self.left_right_text(
                "Cash",
                format_currency(cash_amount, currency='IDR')
            ))
        
        if change is not None:
            lines.append(self.left_right_text(
                "Change",
                format_currency(change, currency='IDR')
            ))
        
        lines.append("")
        return lines
    
    def format_receipt_footer(self, thank_you: str = "Thank you!",
                            message: str = "") -> List[str]:
        """Format receipt footer"""
        lines = [
            self.line_separator(),
            self.center_text(thank_you),
        ]
        
        if message:
            lines.append(self.center_text(message))
        
        lines.extend([
            "",
            "",
            "",
        ])
        
        return lines


class ThermalPrinterService:
    """Manages thermal printer operations"""
    
    def __init__(self):
        """Initialize printer service"""
        self.device: Optional[ThermalPrinterDevice] = None
        self.config: Optional[PrinterConfig] = None
        self.formatter: Optional[ReceiptFormatter] = None
    
    def connect(self, config: PrinterConfig) -> bool:
        """
        Connect to printer with configuration
        
        Args:
            config: PrinterConfig instance
            
        Returns:
            True if successful
        """
        try:
            self.device = ThermalPrinterDevice(config)
            self.device.connect()
            self.config = config
            self.formatter = ReceiptFormatter(width=config.receipt_width)
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def print_receipt(self, receipt_data: Dict) -> bool:
        """
        Print complete receipt
        
        Args:
            receipt_data: Dict with keys:
                - store_name: Store name
                - address: Store address
                - items: List of item dicts
                - subtotal: Subtotal amount
                - discount: Discount amount
                - tax: Tax amount
                - total: Total amount
                - payment_method: Payment method
                - cash_amount: Cash paid (optional)
                - change: Change amount (optional)
                - receipt_time: Receipt time (optional, defaults to now)
                - thank_you: Thank you message (optional)
        """
        if not self.device or not self.device.is_connected:
            raise PrinterOfflineException("Printer not connected")
        
        try:
            # Build receipt content
            receipt_lines = []
            
            # Header
            receipt_lines.extend(self.formatter.format_receipt_header(
                store_name=receipt_data.get('store_name', 'POS System'),
                address=receipt_data.get('address', ''),
                time=receipt_data.get('receipt_time')
            ))
            
            # Items
            receipt_lines.extend(self.formatter.format_receipt_items(
                receipt_data.get('items', [])
            ))
            
            # Totals
            receipt_lines.extend(self.formatter.format_receipt_totals(
                subtotal=receipt_data.get('subtotal', 0),
                discount=receipt_data.get('discount', 0),
                tax=receipt_data.get('tax', 0),
                total=receipt_data.get('total', 0)
            ))
            
            # Payment
            receipt_lines.extend(self.formatter.format_receipt_payment(
                payment_method=receipt_data.get('payment_method', 'Cash'),
                cash_amount=receipt_data.get('cash_amount'),
                change=receipt_data.get('change')
            ))
            
            # Footer
            receipt_lines.extend(self.formatter.format_receipt_footer(
                thank_you=receipt_data.get('thank_you', 'Thank you!'),
                message=receipt_data.get('message', '')
            ))
            
            # Print all lines
            receipt_text = "\n".join(receipt_lines)
            self.device.printer.text(receipt_text)
            
            # Cut paper
            self.device.cut_paper(mode='full')
            
            logger.info("Receipt printed successfully")
            return True
            
        except Exception as e:
            raise PrinterPrintException(f"Receipt print failed: {e}")
    
    def disconnect(self):
        """Disconnect printer"""
        if self.device:
            self.device.disconnect()
            self.device = None
    
    def is_connected(self) -> bool:
        """Check printer connection status"""
        return self.device is not None and self.device.is_connected
