"""
Hardware Configuration Module
Configuration untuk barcode scanner dan thermal printer
"""

import logging
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ScannerConfig:
    """Configuration untuk barcode scanner"""
    name: str = "Generic USB Scanner"
    vendor_id: int = 0x05A3
    product_id: int = 0x0001
    port: Optional[str] = None
    read_timeout: int = 5000
    auto_connect: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScannerConfig':
        """Create dari dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class PrinterConfig:
    """Configuration untuk thermal printer"""
    name: str = "Thermal Printer"
    model: str = "EPSON"
    connection_type: str = "usb"  # usb, network, serial
    vendor_id: int = 0x04B8
    product_id: int = 0x0202
    ip_address: Optional[str] = None
    port: int = 9100
    baudrate: int = 115200
    timeout: int = 5
    receipt_width: int = 32
    auto_cut: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PrinterConfig':
        """Create dari dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


class HardwareConfigManager:
    """Manages hardware configuration dengan file persistence"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path) if config_path else Path("config/hardware.json")
        self.scanners: Dict[str, ScannerConfig] = {}
        self.printers: Dict[str, PrinterConfig] = {}

        # Create directory if needed
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing config
        self.load_config()

    def load_config(self) -> None:
        """Load configuration dari file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    data = json.load(f)

                for name, scanner_data in data.get('scanners', {}).items():
                    self.scanners[name] = ScannerConfig.from_dict(scanner_data)

                for name, printer_data in data.get('printers', {}).items():
                    self.printers[name] = PrinterConfig.from_dict(printer_data)

                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.info("No configuration file found, creating defaults")
                self._create_default_config()
                self.save_config()

        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self._create_default_config()

    def save_config(self) -> None:
        """Save configuration ke file"""
        try:
            data = {
                'scanners': {name: config.to_dict() for name, config in self.scanners.items()},
                'printers': {name: config.to_dict() for name, config in self.printers.items()}
            }

            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"Configuration saved to {self.config_path}")

        except Exception as e:
            logger.error(f"Error saving configuration: {e}")

    def _create_default_config(self) -> None:
        """Create default configuration"""
        self.scanners['default'] = ScannerConfig(
            name="USB Barcode Scanner",
            vendor_id=0x05A3,
            product_id=0x0001
        )

        self.printers['default'] = PrinterConfig(
            name="Epson TM Printer",
            model="EPSON",
            connection_type="usb",
            vendor_id=0x04B8,
            product_id=0x0202,
            receipt_width=32
        )

        logger.info("Created default hardware configuration")

    def get_scanner_config(self, name: str = "default") -> Optional[ScannerConfig]:
        """Get scanner configuration by name"""
        return self.scanners.get(name)

    def get_printer_config(self, name: str = "default") -> Optional[PrinterConfig]:
        """Get printer configuration by name"""
        return self.printers.get(name)

    def add_scanner(self, name: str, config: ScannerConfig) -> None:
        """Add scanner configuration"""
        self.scanners[name] = config
        logger.info(f"Added scanner configuration: {name}")

    def add_printer(self, name: str, config: PrinterConfig) -> None:
        """Add printer configuration"""
        self.printers[name] = config
        logger.info(f"Added printer configuration: {name}")
