# Quick Start Guide - POS Offline System

## System Status ✅ 
**Implementation Complete** - Ready for Development & Testing  
**Date**: December 4, 2025

---

## 📦 What's Installed

### ✅ Core Dependencies
- **PyQt6** (6.10.0) - Desktop GUI framework
- **SQLAlchemy** (2.0.44) - Database ORM
- **cryptography** (46.0.3) - Security & encryption
- **bcrypt** (5.0.0) - Password hashing
- **python-dotenv** (1.2.1) - Environment configuration
- **Pillow** (12.0.0) - Image processing
- **qrcode** (8.2) - QR code generation
- **requests** (2.32.5) - HTTP client

### 📦 Optional (Ready to Install)
```bash
pip install pyusb==1.2.1              # Barcode scanner
pip install python-escpos==3.0        # Thermal printer
pip install pandas==2.1.3             # Data analysis
pip install pytest==7.4.3             # Testing
```

---

## 🚀 Running the Application

### Step 1: Activate Virtual Environment
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Step 2: Initialize Database (First Time Only)
```bash
python scripts/init_db.py
```
✅ Creates SQLite database with all tables

### Step 3: Create Admin User (First Time Only)
```bash
python scripts/create_admin.py
```
Follow prompts:
- Username: `admin`
- Email: `admin@store.com`
- Password: (enter secure password)
- Full Name: (your name)

### Step 4: Start Application
```bash
python src/main.py
```

This will open the POS system with:
- **Sales Screen** (F1) - Main point of sale interface
- Shopping cart with barcode input
- Multiple payment methods
- Receipt printing support

---

## 📁 Project Structure

```
pos/
├── src/                 # Application source code
│   ├── config/         # Configuration (settings, database, logger)
│   ├── models/         # Database ORM models
│   ├── services/       # Business logic & integrations
│   ├── ui/            # User interface screens
│   ├── utils/         # Helper utilities & validators
│   ├── exceptions/    # Custom exceptions
│   └── main.py        # Application entry point
├── scripts/           # Initialization scripts
├── docs/             # Documentation
├── tests/            # Unit tests (ready for development)
├── pos.db            # SQLite database
├── .env.example      # Environment variables template
└── requirements-core.txt
```

---

## ⚙️ Configuration

### 1. Create `.env` File
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```ini
# Store Information
STORE_NAME=Toko Saya
STORE_ADDRESS=Jalan Raya No. 1
STORE_PHONE=+62-812-3456-7890
STORE_EMAIL=contact@toko.com

# Payment Gateway (Midtrans)
MIDTRANS_SERVER_KEY=your_midtrans_server_key
MIDTRANS_CLIENT_KEY=your_midtrans_client_key
MIDTRANS_ENVIRONMENT=sandbox

# Security
SECRET_KEY=your-super-secret-key-for-production
PASSWORD_HASH_ALGORITHM=bcrypt
```

### 2. Get Midtrans Credentials
1. Go to https://dashboard.midtrans.com
2. Sign up or login
3. Get **Server Key** and **Client Key** from Dashboard
4. Use **Sandbox** for testing
5. Add to `.env` file

---

## 🛒 Sales Screen Usage

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| **F1** | Switch to Sales |
| **F2** | Switch to Inventory |
| **F3** | Process Cash Payment |
| **F4** | Process Card/E-wallet |
| **Esc** | Clear Cart |
| **Enter** | Look up product by barcode |

### How to Process a Sale

1. **Input Product**
   - Scan barcode or type SKU
   - Press Enter
   - Set quantity
   - Click "Tambah ke Keranjang"

2. **Review Cart**
   - Items appear in shopping cart table
   - See real-time totals
   - Remove items with X button

3. **Process Payment**
   - **Cash**: Press F3 → Enter amount → Get change
   - **Card/E-wallet**: Press F4 → Select method
   - Both options trigger receipt printing

---

## 🏦 Payment Methods Supported

### Available Methods
✅ Bank Transfer (11+ Indonesian banks)  
✅ QRIS (Instant payment code)  
✅ E-wallets (GoPay, OVO, DANA, ShopeePay)  
✅ Credit/Debit Cards  
✅ Buy Now Pay Later (Installments)  
✅ Indomaret/Alfamart (OTC)  
✅ Cash  

All powered by **Midtrans** with 25+ payment options.

---

## 🔧 Development Setup

### Install Development Tools
```bash
pip install pytest==7.4.3          # Testing framework
pip install black==23.12.0         # Code formatter
pip install pylint==3.0.3          # Linter
pip install mypy==1.7.1            # Type checker
```

### Run Tests (When Ready)
```bash
pytest tests/ -v                    # Run all tests
pytest tests/ --cov                 # With coverage report
```

### Format Code
```bash
black src/                          # Auto-format all source
```

---

## 🔌 Hardware Integration (Optional)

### Barcode Scanner
```python
from src.services.barcode_scanner_service import BarcodeScannerService

scanner = BarcodeScannerService()
scanner.auto_detect_and_connect()
scanner.start_scanning()
```

### Thermal Printer
```python
from src.services.thermal_printer_service import ThermalPrinterService, PrinterConfig, PrinterConnection

printer_config = PrinterConfig(
    model="epson",
    connection_type=PrinterConnection.USB,
    vendor_id=0x04b8,
    product_id=0x0202
)

printer = ThermalPrinterService()
printer.connect(printer_config)
printer.print_receipt(receipt_data)
```

---

## 📊 Database Models

Implemented ORM models:
- **Product** - Items for sale (SKU, price, stock)
- **Customer** - Customer profiles (loyalty points, history)
- **Transaction** - Sales records (items, payment, status)
- **User** - Staff accounts (roles, permissions)
- **Inventory** - Stock tracking (quantities, movement)
- **Payment** - Payment records (method, status, reference)

---

## 📚 Documentation

- **IMPLEMENTATION_STATUS.md** - Complete implementation details
- **PAYMENT_GATEWAY.md** - Midtrans integration guide
- **README.md** - Project overview
- **Code docstrings** - Inline documentation

---

## 🐛 Troubleshooting

### Issue: PyQt6 window won't open
**Solution**: Ensure X11/display is available. For headless, use unit tests instead.

### Issue: Database locked
**Solution**: Close any other instances and restart.

### Issue: Payment gateway error
**Solution**: Check Midtrans credentials in `.env` and test with sandbox key.

### Issue: Barcode scanner not detected
**Solution**: Install pyusb and check USB device permissions.

---

## 📞 Next Steps

1. **Test sales screen**: Run app and process a sample sale
2. **Configure store info**: Update `.env` with your store details
3. **Set payment gateway**: Add Midtrans credentials for payments
4. **Create users**: Use admin script to add staff accounts
5. **Test payments**: Use Midtrans sandbox credentials for testing
6. **Add products**: Implement product management screen
7. **Deploy**: When ready for production, update configurations

---

## ✨ Features Ready Now

- ✅ Sales point-of-sale interface
- ✅ Shopping cart management
- ✅ Multiple payment methods
- ✅ Payment gateway integration
- ✅ Receipt printing support
- ✅ Barcode scanner service
- ✅ User authentication (setup)
- ✅ Database with 6 ORM models
- ✅ Logging & error handling
- ✅ Hardware configuration

---

## 🎯 Coming Soon

- 📋 Inventory management screen
- 👥 Customer management screen  
- 📊 Reports & analytics
- ⚙️ Settings screen
- 🔐 Advanced user roles
- ☁️ Cloud sync capability
- 📱 Mobile app integration

---

**Happy POS-ing! 🎉**

For detailed technical documentation, see `IMPLEMENTATION_STATUS.md`

---
*Generated: 2025-12-04 | POS Offline System v1.0-beta*
