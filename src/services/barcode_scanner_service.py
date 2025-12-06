"""
Barcode Scanner Service for offline POS system
Handles USB HID barcode scanner integration with threading for concurrent scanning
"""

import threading
import logging
import time
from dataclasses import dataclass
from typing import Optional, Callable, List
from queue import Queue

try:
    import usb.core
    import usb.util
    HAS_PYUSB = True
except ImportError:
    HAS_PYUSB = False

from src.exceptions.hardware_exceptions import (
    ScannerException,
    ScannerNotConnectedException,
    ScannerDisconnectedException,
    ScannerReadException
)
from src.utils.validators import validate_barcode


logger = logging.getLogger(__name__)


@dataclass
class ScanData:
    """Container for barcode scan data"""
    barcode: str
    timestamp: float
    device_id: str
    raw_data: bytes


class BarcodeScannerDevice:
    """Represents a physical barcode scanner device"""
    
    # Standard USB HID keyboard codes for numeric input
    HID_KEYCODES = {
        0x27: '0', 0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4',
        0x22: '5', 0x23: '6', 0x24: '7', 0x25: '8', 0x26: '9',
        0x2D: '-', 0x2E: '=', 0x38: '[', 0x30: '{', 0x48: '*',
    }
    
    def __init__(self, vendor_id: int, product_id: int, timeout: int = 1000):
        """
        Initialize scanner device
        
        Args:
            vendor_id: USB vendor ID
            product_id: USB product ID
            timeout: Read timeout in milliseconds
        """
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.timeout = timeout
        self.device = None
        self.endpoint = None
        self.is_connected = False
        self.device_id = f"{vendor_id:04x}:{product_id:04x}"
        
    def connect(self) -> bool:
        """
        Connect to the scanner device
        
        Returns:
            True if connection successful, False otherwise
        """
        if not HAS_PYUSB:
            logger.error("pyusb not installed")
            raise ScannerException("pyusb library required")
            
        try:
            self.device = usb.core.find(
                idVendor=self.vendor_id,
                idProduct=self.product_id
            )
            
            if self.device is None:
                raise ScannerNotConnectedException(
                    f"Scanner {self.device_id} not found"
                )
            
            # Try to detach kernel driver if necessary
            try:
                if self.device.is_kernel_driver_active(0):
                    self.device.detach_kernel_driver(0)
            except usb.core.USBError:
                pass  # Windows doesn't have kernel drivers
            
            # Set configuration
            self.device.set_configuration()
            
            # Get HID interface for barcode scanner
            cfg = self.device.get_active_configuration()
            intf = cfg[(0, 0)]
            
            # Find interrupt IN endpoint
            self.endpoint = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(
                    e.bEndpointAddress
                ) == usb.util.ENDPOINT_IN
            )
            
            if self.endpoint is None:
                raise ScannerException("No input endpoint found")
            
            self.is_connected = True
            logger.info(f"Scanner {self.device_id} connected")
            return True
            
        except usb.core.USBError as e:
            self.is_connected = False
            raise ScannerNotConnectedException(f"USB error: {e}")
    
    def read_scan(self) -> Optional[ScanData]:
        """
        Read barcode from scanner
        
        Returns:
            ScanData if successful, None if no data
            
        Raises:
            ScannerDisconnectedException: If device disconnected
            ScannerReadException: If read error occurs
        """
        if not self.is_connected or self.device is None:
            raise ScannerDisconnectedException("Scanner not connected")
        
        try:
            data = self.device.read(
                self.endpoint.bEndpointAddress,
                self.endpoint.wMaxPacketSize,
                timeout=self.timeout
            )
            
            # Convert HID codes to ASCII characters
            barcode = ""
            for byte in data:
                if byte in self.HID_KEYCODES:
                    barcode += self.HID_KEYCODES[byte]
            
            if barcode:
                return ScanData(
                    barcode=barcode.strip(),
                    timestamp=time.time(),
                    device_id=self.device_id,
                    raw_data=bytes(data)
                )
            return None
            
        except usb.core.USBError as e:
            if "No such device" in str(e):
                self.is_connected = False
                raise ScannerDisconnectedException(f"Scanner disconnected: {e}")
            raise ScannerReadException(f"Read error: {e}")
    
    def disconnect(self):
        """Safely disconnect scanner"""
        try:
            if self.device:
                usb.util.release_interface(self.device, 0)
            self.is_connected = False
            logger.info(f"Scanner {self.device_id} disconnected")
        except Exception as e:
            logger.warning(f"Disconnect error: {e}")


class BarcodeScannerService:
    """Manages barcode scanner with thread-safe scanning and callbacks"""
    
    # Common scanner VID/PID combinations
    SCANNER_DEVICES = [
        (0x0c2e, 0x0008),  # Honeywell
        (0x05e0, 0x1200),  # Symbol
        (0x1690, 0x0701),  # Metrologic
        (0x067b, 0x2303),  # Prolific USB
    ]
    
    def __init__(self, auto_reconnect: bool = True):
        """
        Initialize scanner service
        
        Args:
            auto_reconnect: Automatically reconnect if disconnected
        """
        self.device: Optional[BarcodeScannerDevice] = None
        self.auto_reconnect = auto_reconnect
        self.is_scanning = False
        self.scan_thread: Optional[threading.Thread] = None
        self.scan_queue = Queue()
        self.callbacks: List[Callable[[ScanData], None]] = []
        self._lock = threading.Lock()
        
    def add_scan_callback(self, callback: Callable[[ScanData], None]):
        """Register callback for scan events"""
        self.callbacks.append(callback)
    
    def remove_scan_callback(self, callback: Callable[[ScanData], None]):
        """Unregister callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def auto_detect_and_connect(self) -> bool:
        """
        Auto-detect and connect to first available scanner
        
        Returns:
            True if connection successful
        """
        if not HAS_PYUSB:
            raise ScannerException("pyusb library required for auto-detection")
        
        for vid, pid in self.SCANNER_DEVICES:
            try:
                device = BarcodeScannerDevice(vid, pid)
                if device.connect():
                    self.device = device
                    logger.info(f"Auto-detected scanner: {device.device_id}")
                    return True
            except ScannerNotConnectedException:
                continue
        
        raise ScannerNotConnectedException("No scanner auto-detected")
    
    def connect(self, vendor_id: int, product_id: int) -> bool:
        """
        Connect to specific scanner
        
        Args:
            vendor_id: USB vendor ID
            product_id: USB product ID
            
        Returns:
            True if successful
        """
        try:
            self.device = BarcodeScannerDevice(vendor_id, product_id)
            return self.device.connect()
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def start_scanning(self):
        """Start continuous barcode scanning in background thread"""
        with self._lock:
            if self.is_scanning:
                return
            
            if not self.device or not self.device.is_connected:
                raise ScannerNotConnectedException("Scanner not connected")
            
            self.is_scanning = True
            self.scan_thread = threading.Thread(
                target=self._scan_loop,
                daemon=True
            )
            self.scan_thread.start()
            logger.info("Scanner polling started")
    
    def stop_scanning(self):
        """Stop continuous scanning"""
        with self._lock:
            self.is_scanning = False
        
        if self.scan_thread:
            self.scan_thread.join(timeout=5)
        logger.info("Scanner polling stopped")
    
    def _scan_loop(self):
        """Main scanning loop (runs in background thread)"""
        consecutive_errors = 0
        
        while self.is_scanning:
            try:
                scan_data = self.device.read_scan()
                if scan_data:
                    consecutive_errors = 0
                    # Validate barcode
                    is_valid, msg = validate_barcode(scan_data.barcode)
                    if is_valid:
                        self.scan_queue.put(scan_data)
                        # Call registered callbacks
                        for callback in self.callbacks:
                            try:
                                callback(scan_data)
                            except Exception as e:
                                logger.error(f"Callback error: {e}")
                    else:
                        logger.debug(f"Invalid barcode: {msg}")
                
                time.sleep(0.01)  # Prevent busy waiting
                
            except ScannerDisconnectedException as e:
                consecutive_errors += 1
                logger.warning(f"Scanner disconnected: {e}")
                
                if self.auto_reconnect and consecutive_errors < 3:
                    logger.info("Attempting to reconnect...")
                    try:
                        if self.device.connect():
                            consecutive_errors = 0
                            logger.info("Reconnection successful")
                    except Exception as reconnect_error:
                        logger.error(f"Reconnection failed: {reconnect_error}")
                else:
                    self.is_scanning = False
                    
            except ScannerReadException as e:
                logger.error(f"Read error: {e}")
                consecutive_errors += 1
                if consecutive_errors >= 5:
                    self.is_scanning = False
            
            except Exception as e:
                logger.error(f"Unexpected error in scan loop: {e}")
                self.is_scanning = False
    
    def get_next_scan(self, timeout: Optional[float] = None) -> Optional[ScanData]:
        """
        Get next scan from queue
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            ScanData or None if queue empty
        """
        try:
            return self.scan_queue.get(timeout=timeout)
        except:
            return None
    
    def disconnect(self):
        """Disconnect scanner and stop scanning"""
        self.stop_scanning()
        if self.device:
            self.device.disconnect()
            self.device = None
        logger.info("Scanner service disconnected")
    
    def is_connected(self) -> bool:
        """Check if scanner is connected"""
        return self.device is not None and self.device.is_connected
