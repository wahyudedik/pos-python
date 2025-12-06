"""
Create Admin User Script
Create admin user untuk system
"""

import sys
from pathlib import Path
import getpass

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
from src.config.logger import setup_logging, get_logger
from src.config.database import SessionLocal, init_db
from src.models.user import User, UserRole

logger = get_logger(__name__)


def create_admin_user():
    """Create admin user"""
    try:
        setup_logging()
        logger.info("Creating admin user...")
        
        # Initialize database
        init_db()
        
        # Get input
        username = input("Username [admin]: ").strip() or "admin"
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ")
        password_confirm = getpass.getpass("Confirm Password: ")
        
        if password != password_confirm:
            print("✗ Passwords do not match")
            sys.exit(1)
        
        # Hash password
        import bcrypt
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # Create user
        db = SessionLocal()
        try:
            # Check if user exists
            existing = db.query(User).filter(User.username == username).first()
            if existing:
                print(f"✗ User {username} already exists")
                sys.exit(1)
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                full_name=input("Full Name: ").strip() or username,
                role=UserRole.ADMIN,
                is_active=True
            )
            
            db.add(user)
            db.commit()
            
            logger.info(f"Admin user created: {username}")
            print(f"✓ Admin user '{username}' created successfully!")
            
        finally:
            db.close()
        
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Install bcrypt: pip install bcrypt")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Error creating admin user: {e}", exc_info=True)
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_admin_user()
