# POS Offline System - Python

Sistem Point of Sale (POS) offline modern untuk UMKM dan toko retail Indonesia. Aplikasi desktop standalone dengan dukungan multiple payment gateway, inventory management real-time, dan comprehensive reporting.

## 🎯 Tujuan Sistem

Menyediakan solusi POS yang **affordable, reliable, dan easy-to-use** untuk membantu UMKM dan toko retail mengelola penjualan, inventory, dan keuangan dengan lebih efisien.

## ✨ Fitur-Fitur Utama

### Tier 1: Core Features (MVP)
- ✅ **Point of Sale (Kasir)** - Interface penjualan cepat dengan barcode scanner support
- ✅ **Kalkulasi Otomatis** - Subtotal, pajak (PPN), diskon per item/transaksi
- ✅ **Multiple Payment Methods** - Tunai, kartu debit/kredit, e-wallet, transfer bank
- ✅ **Inventory Real-time** - Stock tracking otomatis, reorder alerts, kategori produk
- ✅ **Receipt/Struk** - Cetak thermal & digital, online/offline support
- ✅ **Multi-user Login** - Role-based access (Admin/Manager/Cashier/Operator)
- ✅ **Payment Gateway Integration** - Midtrans untuk online payment & settlement
- ✅ **Laporan Penjualan** - Harian, mingguan, bulanan dengan profit calculation
- ✅ **Database Offline** - SQLite untuk single-toko, PostgreSQL-ready untuk scaling

### Tier 2: Value-Add Features
- 🔄 **Customer Profile & History** - Master customer, purchase tracking, repeat customer identification
- 🎁 **Loyalty Program** - Points reward system & discount tiers
- 📊 **Advanced Reports** - Best sellers, slow movers, seasonal trends, KPI dashboard
- 🏷️ **Barcode Management** - Generate, print, manage barcode/SKU
- 🔐 **Audit Log** - Track semua transaksi & user actions
- 💾 **Automated Backup** - Daily backup & restore functionality

### Tier 3: Enterprise Features
- 🏪 **Multi-Toko Support** - Centralized reporting, transfer stok antar toko
- 🌐 **Cloud Sync** - Optional cloud backup & multi-device access
- 📱 **Mobile Integration** - Barcode scanner app, mobile reporting

## 🛠️ Technology Stack

### Frontend
- **PyQt6** - Modern desktop GUI framework
- **Python 3.9+** - Core programming language

### Backend & Database
- **SQLAlchemy** - ORM untuk database abstraction
- **SQLite** - Local database (offline-first)

### Payment Gateway
- **Midtrans** - 25+ payment methods dengan real-time settlement

### Supporting Libraries
- **python-escpos** - Thermal printer control
- **pyusb** - USB barcode scanner
- **qrcode** - QR code generation
- **cryptography** - Data encryption

## 💳 Payment Gateway Integration

### Midtrans Features:
- ✅ 25+ payment methods (Bank Transfer, E-wallet, Credit Card, OTC, BNPL)
- ✅ Settlement real-time & reconciliation otomatis
- ✅ Dashboard powerful & reporting lengkap
- ✅ Native POS integration support
- ✅ 13 tahun track record di Indonesia

**Biaya:** Gratis setup, ~1% GMV untuk transaction fees

## 📦 Installation

### Prerequisites
- Python 3.9 atau lebih tinggi
- pip (Python package manager)

### Step 1: Clone Project
```bash
cd d:\PROJECT\PYTHON\pos
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```bash
cp .env.example .env
# Edit .env dengan credentials Anda
```

### Step 5: Initialize Database
```bash
python scripts/init_db.py
```

### Step 6: Create Admin User
```bash
python scripts/create_admin.py
```

### Step 7: Run Application
```bash
python src/main.py
```

## 🚀 Quick Start

### First Time Setup
1. Start aplikasi dengan `python src/main.py`
2. Login dengan admin credentials
3. Setup toko di Settings
4. Add payment methods
5. Import atau add produk di Inventory menu

### Daily Operation
1. Operator login & start selling
2. Scan barcode atau manual input SKU
3. Add quantity & apply discount jika ada
4. Select payment method
5. Process payment
6. Print receipt
7. System automatically update inventory

## 📁 Project Structure

```
pos/
├── src/
│   ├── main.py                          # Application entry point
│   ├── config/
│   │   ├── settings.py                  # Global configuration
│   │   ├── database.py                  # Database connection
│   │   ├── logger.py                    # Logging setup
│   │   └── payment_config.py            # Midtrans configuration
│   ├── models/
│   │   ├── product.py                   # Product ORM model
│   │   ├── customer.py                  # Customer model
│   │   ├── transaction.py               # Sales transaction model
│   │   ├── user.py                      # User/operator model
│   │   ├── inventory.py                 # Inventory tracking model
│   │   └── payment.py                   # Payment records model
│   ├── services/
│   │   ├── sales_service.py             # Sales business logic
│   │   ├── inventory_service.py         # Inventory operations
│   │   ├── customer_service.py          # Customer management
│   │   ├── payment_service.py           # Payment processing
│   │   ├── auth_service.py              # Authentication
│   │   ├── report_service.py            # Report generation
│   │   ├── barcode_scanner_service.py   # Scanner integration
│   │   ├── thermal_printer_service.py   # Printer integration
│   │   └── midtrans_gateway.py          # Midtrans API wrapper
│   ├── repositories/
│   │   ├── base_repository.py           # Base class for repos
│   │   ├── product_repository.py        # Product DB ops
│   │   ├── customer_repository.py       # Customer DB ops
│   │   └── transaction_repository.py    # Transaction DB ops
│   ├── ui/
│   │   ├── main_window.py               # Main app window
│   │   ├── screens/
│   │   │   ├── sales_screen.py          # Point of Sale screen
│   │   │   ├── inventory_screen.py      # Inventory management
│   │   │   ├── customer_screen.py       # Customer management
│   │   │   ├── reports_screen.py        # Reports & analytics
│   │   │   ├── settings_screen.py       # Settings
│   │   │   └── login_screen.py          # Login
│   │   ├── dialogs/
│   │   │   ├── payment_dialog.py        # Payment dialog
│   │   │   └── receipt_dialog.py        # Receipt preview
│   │   └── widgets/
│   │       └── cart_widget.py           # Cart widget
│   ├── utils/
│   │   ├── validators.py                # Input validation
│   │   ├── formatters.py                # Data formatting
│   │   ├── currency.py                  # Currency utilities
│   │   ├── exceptions.py                # Custom exceptions
│   │   ├── hardware_config.py           # Hardware configuration
│   │   └── helpers.py                   # Helper functions
│   └── exceptions/
│       ├── custom_exceptions.py         # App exceptions
│       └── hardware_exceptions.py       # Hardware exceptions
├── tests/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_repositories.py
├── docs/
│   └── PAYMENT_GATEWAY.md               # Payment integration docs
├── config/
│   └── hardware.json                    # Hardware device config
├── scripts/
│   ├── init_db.py                       # Database initialization
│   └── create_admin.py                  # Admin user creation
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment template
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## 📞 Support & Contact

Untuk pertanyaan atau bug reports:
- GitHub Issues
- Email: support@pos-system.id
- Documentation: `docs/USER_GUIDE.md`

## 📄 License

MIT License

---

**Version:** 1.0.0-beta
**Status:** Under Development
**Last Updated:** Desember 2025
