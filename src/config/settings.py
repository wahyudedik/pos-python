"""
Application Settings Configuration
Global configuration management untuk POS system
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===== APP SETTINGS =====
APP_NAME = os.getenv("APP_NAME", "POS Offline System")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ===== PATHS =====
BASE_DIR = Path(__file__).parent.parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
BACKUPS_DIR = BASE_DIR / "backups"
CONFIG_DIR = BASE_DIR / "config"

# Create directories if not exist
for directory in [DATA_DIR, LOGS_DIR, BACKUPS_DIR, CONFIG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ===== DATABASE =====
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pos.db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() == "true"
DATABASE_POOL_SIZE = 10
DATABASE_POOL_RECYCLE = 3600

# ===== STORE CONFIGURATION =====
STORE_NAME = os.getenv("STORE_NAME", "Toko Saya")
STORE_ADDRESS = os.getenv("STORE_ADDRESS", "")
STORE_PHONE = os.getenv("STORE_PHONE", "")
STORE_EMAIL = os.getenv("STORE_EMAIL", "")
STORE_TAX_ID = os.getenv("STORE_TAX_ID", "")
STORE_CURRENCY = os.getenv("STORE_CURRENCY", "IDR")
CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "Rp ")
TAX_RATE = float(os.getenv("TAX_RATE", "0.1"))  # 10% default

# ===== SECURITY =====
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
PASSWORD_HASH_ALGORITHM = os.getenv("PASSWORD_HASH_ALGORITHM", "bcrypt")
SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))

# ===== LOGGING =====
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")
LOG_FILE = LOGS_DIR / os.getenv("LOG_FILE", "pos.log")
LOG_ROTATION_SIZE = 10485760  # 10MB
LOG_BACKUP_COUNT = 5

# ===== UI/UX =====
THEME = os.getenv("THEME", "dark")
LANGUAGE = os.getenv("LANGUAGE", "id")
DATE_FORMAT = os.getenv("DATE_FORMAT", "DD/MM/YYYY")
TIME_FORMAT = os.getenv("TIME_FORMAT", "HH:mm:ss")
CURRENCY_FORMAT = os.getenv("CURRENCY_FORMAT", "IDR")
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# ===== PRINTER =====
PRINTER_THERMAL_NAME = os.getenv("PRINTER_THERMAL_NAME", "Thermal Printer")
PRINTER_THERMAL_PAPER_WIDTH = int(os.getenv("PRINTER_THERMAL_PAPER_WIDTH", "80"))

# ===== BACKUP =====
BACKUP_ENABLED = os.getenv("BACKUP_ENABLED", "True").lower() == "true"
BACKUP_SCHEDULE = os.getenv("BACKUP_SCHEDULE", "daily")
BACKUP_TIME = os.getenv("BACKUP_TIME", "02:00")
BACKUP_RETENTION_DAYS = int(os.getenv("BACKUP_RETENTION_DAYS", "30"))
BACKUP_PATH = BACKUPS_DIR

# ===== FEATURE FLAGS =====
FEATURE_CUSTOMER_LOYALTY = os.getenv("FEATURE_CUSTOMER_LOYALTY", "True").lower() == "true"
FEATURE_ONLINE_PAYMENTS = os.getenv("FEATURE_ONLINE_PAYMENTS", "True").lower() == "true"
FEATURE_MULTI_TOKO = os.getenv("FEATURE_MULTI_TOKO", "False").lower() == "true"
FEATURE_CLOUD_SYNC = os.getenv("FEATURE_CLOUD_SYNC", "False").lower() == "true"

# ===== PAYMENT GATEWAY =====
MIDTRANS_ENABLED = os.getenv("MIDTRANS_ENABLED", "True").lower() == "true"
MIDTRANS_ENVIRONMENT = os.getenv("MIDTRANS_ENVIRONMENT", "sandbox")
MIDTRANS_SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY", "")
MIDTRANS_CLIENT_KEY = os.getenv("MIDTRANS_CLIENT_KEY", "")
MIDTRANS_MERCHANT_ID = os.getenv("MIDTRANS_MERCHANT_ID", "")
