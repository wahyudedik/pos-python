"""
Database Initialization Script
Initialize database dengan sample data
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
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


def init_database():
    """Initialize database"""
    try:
        setup_logging()
        logger.info("Initializing database...")
        
        # Create all tables
        init_db()
        
        logger.info("Database initialized successfully!")
        print("✓ Database initialized")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_database()
