"""
Main Entry Point
POS Offline System Application
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config.logger import setup_logging, get_logger
from src.config.database import init_db

# Import all models to register them with Base
from src.models.product import Product
from src.models.customer import Customer
from src.models.transaction import Transaction
from src.models.user import User
from src.models.inventory import Inventory
from src.models.payment import Payment

logger = get_logger(__name__)


def main():
    """Main application entry point"""
    try:
        # Setup logging
        setup_logging()
        logger.info("=== POS Offline System Starting ===")

        # Initialize database
        logger.info("Initializing database...")
        init_db()

        # Import PyQt6 after logging setup
        from PyQt6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow

        # Create application
        app = QApplication(sys.argv)
        
        # Create main window
        logger.info("Creating main window...")
        main_window = MainWindow()
        main_window.show()

        logger.info("Application started successfully")

        # Run application
        sys.exit(app.exec())

    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}")
        print("Please install required packages:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
