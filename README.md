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

### Frontend (GUI)
- **PyQt6** v6.6+ - Modern desktop GUI framework dengan native look & feel
- **qdarkstyle** - Dark theme untuk professional appearance
- **Custom Widgets** - Reusable components untuk konsistensi UI

### Backend & Processing
- **Python** 3.10+ - Core programming language
- **SQLAlchemy** 2.0+ - ORM untuk database abstraction & query building
- **pandas** - Data processing untuk reporting
- **numpy** - Numerical computing

### Database
- **SQLite** - Local database (offline-first, zero-config)
- **PostgreSQL** (ready) - Untuk multi-location scaling

### Payment Gateway Integration
- **Midtrans** SDK v1.4+ - 25+ payment methods integration
- **cryptography** - Secure payment data encryption
- **requests** - HTTP client untuk API calls

### Hardware Integration
- **python-escpos** - Thermal printer control (receipt printing)
- **pyusb** - USB barcode scanner integration
- **python-barcode** - Generate barcodes & QR codes
- **Pillow** - Image processing untuk barcode/receipt

### Development & Testing
- **pytest** - Unit testing framework
- **pytest-cov** - Code coverage measurement
- **black** - Code formatter
- **flake8** - Code linter
- **PyInstaller** - Build standalone executables

### Utilities
- **python-dotenv** - Environment variable management
- **python-dateutil** - Date/time utilities
- **pytz** - Timezone handling
- **requests** - HTTP client library

### Distribution & Deployment
- **PyInstaller** - Create .exe executable
- **NSIS** - Create professional Windows installer
- **setuptools** - Python packaging

---

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│         POS System Architecture         │
└─────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│     User Interface (PyQt6 Desktop GUI)   │
├──────────────────────────────────────────┤
│ • Sales Screen      • Inventory Screen   │
│ • Reports Screen    • Settings Screen    │
│ • Login Screen      • Customer Screen    │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│   Business Logic Layer (Services)        │
├──────────────────────────────────────────┤
│ • SalesService      • PaymentService     │
│ • InventoryService  • CustomerService    │
│ • AuthService       • ReportService      │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│   Data Access Layer (Repositories)       │
├──────────────────────────────────────────┤
│ • ProductRepository • TransactionRepo    │
│ • CustomerRepository• UserRepository     │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│      Database Layer (SQLAlchemy ORM)     │
├──────────────────────────────────────────┤
│ Models: Product, Customer, Transaction   │
│ Models: User, Inventory, Payment         │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│    SQLite Database (Offline-First)       │
├──────────────────────────────────────────┤
│ File: pos.db (local, portable, simple)   │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│    External Integrations (Optional)      │
├──────────────────────────────────────────┤
│ • Midtrans Payment Gateway               │
│ • USB Barcode Scanner                    │
│ • Thermal Printer (ESCPOS)               │
└──────────────────────────────────────────┘
```

---

## 💳 Payment Gateway Integration

### Midtrans Features
- **25+ Payment Methods** - Bank Transfer, E-wallet, Credit Card, OTC, BNPL
- **Real-time Settlement** - Auto settlement setiap hari
- **Reconciliation Otomatis** - Matching transactions dengan penjualan
- **Dashboard Powerful** - Monitor penjualan & settlement
- **Native POS Support** - Optimized untuk POS systems
- **13 Tahun Track Record** - Terpercaya di Indonesia

### Integration Points
- Payment button di Sales Screen
- Transaction recording otomatis
- Settlement reports di Reports menu
- Test connection di Settings → Test Gateway

### Biaya Struktur
- **Setup Fee**: Gratis
- **Admin Fee**: Bervariasi per bank (~2,500-5,000)
- **Transaction Fee**: ~1-2% dari GMV (negotiable for high volume)
- **Settlement**: Free dan otomatis daily

---

## 🔒 Security & Data Protection

### Data Security
- **Encrypted Database** - Optional encryption untuk sensitive data
- **User Authentication** - Password hashing dengan bcrypt
- **Audit Logging** - Track semua transaksi & user actions
- **Session Management** - Secure session handling
- **Environment Variables** - Sensitive data di .env (not in code)

### Network Security (Future)
- **HTTPS** - Untuk cloud sync features
- **API Authentication** - Token-based untuk external API
- **Data Encryption** - TLS untuk data in-transit

---

## 📈 Performance & Scalability

### Current (Single Location)
- **Database**: SQLite (File-based, ~50-100K transactions/year)
- **Performance**: Sub-second response for all operations
- **Concurrent Users**: 1-5 operators per toko
- **Data Retention**: Unlimited (local storage)

### Future (Multi Location)
- **Database**: PostgreSQL (Network database)
- **Architecture**: Centralized reporting, distributed sales
- **Sync**: Real-time or scheduled sync between locations
- **Scaling**: Unlimited locations & users

## 📦 Installation & Setup

### Prerequisites
- **Python** 3.10 atau lebih tinggi
- **pip** (Python package manager)
- **Git** untuk version control
- **PyInstaller** (diinstall otomatis saat build)

### Option 1: Clone dari GitHub

#### Step 1: Clone Repository
```bash
# Clone project
git clone https://github.com/wahyudedik/pos-python.git
cd pos-python

# Atau jika sudah ada folder lokal
cd d:\PROJECT\PYTHON\pos
```

#### Step 2: Create Virtual Environment
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Setup Environment Variables
```bash
# Copy template environment file
cp .env.example .env

# Edit .env dengan credentials Anda (text editor)
# - Midtrans API Keys
# - Database path
# - Printer settings
# - Scanner settings
```

#### Step 5: Initialize Database
```bash
python scripts/init_db.py
```

#### Step 6: Create Admin User (Optional)
```bash
python scripts/create_admin.py
# Follow prompts untuk create admin account
```

---

## 🚀 Development Setup

### Running Application in Development

#### Option 1: Direct Run (Recommended for Dev)
```bash
# Activate virtual environment dulu
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Kemudian run aplikasi
python src/main.py
```

#### Option 2: Run with Debug Logging
```bash
# Set logging level untuk debug
set DEBUG=1
python src/main.py

# Atau di PowerShell
$env:DEBUG=1
python src/main.py
```

#### Option 3: Run Specific Module
```bash
# Test module tertentu
python -m pytest tests/test_models.py -v

# Run dengan coverage
pytest --cov=src tests/
```

### Development Workflow

1. **Edit Code**
   - Buat branch baru untuk fitur: `git checkout -b feature/nama-fitur`
   - Edit file sesuai kebutuhan
   - Test secara lokal dengan `python src/main.py`

2. **Test Changes**
   ```bash
   # Run unit tests
   pytest tests/ -v
   
   # Check code style
   flake8 src/
   
   # Format code
   black src/
   ```

3. **Commit & Push**
   ```bash
   git add .
   git commit -m "Feature: Deskripsi perubahan"
   git push origin feature/nama-fitur
   ```

4. **Create Pull Request**
   - Go to GitHub
   - Create PR dengan deskripsi detail
   - Wait for review

---

## 🔄 Update Version & Build Executable

### Version Management

#### Step 1: Update Version Number

Edit file `src/config/settings.py`:
```python
# Ubah version number
APP_VERSION = "1.1.0"  # Format: MAJOR.MINOR.PATCH

# Atau edit di setup.py
version="1.1.0"
```

#### Step 2: Update Changelog
```bash
# Add entry ke CHANGELOG.md
# Format:
# ## [1.1.0] - 2025-12-06
# ### Added
# - New feature description
# ### Fixed
# - Bug fix description
```

#### Step 3: Tag Release
```bash
# Create git tag
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0

# Atau tanpa push
git tag v1.1.0
```

### Building New Executable

#### Quick Build (Recommended)
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run quick build script
.\quick_build.ps1

# Tunggu 10-20 menit untuk first build
# Output: dist\POS-System.exe
```

#### Advanced Build (dengan Options)
```bash
# Build dengan custom options
.\build_installer.ps1

# Atau untuk advanced users
.\build_installer.ps1 -CleanBuild
.\build_installer.ps1 -BuildType exe
.\build_installer.ps1 -SkipNSIS
```

#### Manual Build
```bash
# Install PyInstaller jika belum
pip install PyInstaller

# Build executable
pyinstaller --onefile --windowed --name "POS-System" src/main.py

# Output akan di: dist\POS-System.exe
```

### Distribution & Release

#### Step 1: Test Executable
```bash
# Double-click executable
dist\POS-System.exe

# Atau run dari PowerShell
.\dist\POS-System.exe

# Verify:
# ✓ Aplikasi launch tanpa error
# ✓ Database auto-created
# ✓ Semua features working
```

#### Step 2: Create Release Build
```bash
# Clean build untuk release
.\build_installer.ps1 -CleanBuild

# Atau manual
rmdir /s build dist
pyinstaller --onefile --windowed --name "POS-System" src/main.py
```

#### Step 3: Prepare Distribution Package
```bash
# Organize files untuk distribution
New-Item -ItemType Directory -Path "releases\v1.1.0" -Force

# Copy executable
Copy-Item "dist\POS-System.exe" "releases\v1.1.0\"

# Copy docs
Copy-Item "README.md", ".env.example", "LICENSE" "releases\v1.1.0\"

# Create ZIP
Compress-Archive -Path "releases\v1.1.0" -DestinationPath "releases\POS-System-v1.1.0.zip"
```

#### Step 4: Release to User
```bash
# Option 1: Direct send executable
# Send: releases\v1.1.0\POS-System.exe

# Option 2: Send ZIP package
# Send: releases\POS-System-v1.1.0.zip
# User: Extract & double-click exe

# Option 3: Create installer (memerlukan NSIS)
makensis.exe installer\POS-System-Installer.nsi
# Result: dist\POS-System-Installer-v1.1.0.exe
```

### Versioning Strategy

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR** - Breaking changes, significant features
  - Contoh: 1.0.0 → 2.0.0
  
- **MINOR** - New features, backward compatible
  - Contoh: 1.0.0 → 1.1.0
  
- **PATCH** - Bug fixes, small improvements
  - Contoh: 1.0.0 → 1.0.1

**Example Release Cycle**:
```
v1.0.0 - Initial release
v1.0.1 - Bug fix
v1.0.2 - Bug fix
v1.1.0 - New features (inventory export)
v1.1.1 - Bug fix
v2.0.0 - Major rewrite (cloud sync)
```

### CI/CD Checklist (Before Release)

- [ ] Update version number di `src/config/settings.py`
- [ ] Update `CHANGELOG.md` dengan changes
- [ ] Run tests: `pytest tests/ -v`
- [ ] Run code style check: `flake8 src/`
- [ ] Clean build: `.build_installer.ps1 -CleanBuild`
- [ ] Test executable: `dist\POS-System.exe`
- [ ] Verify all features working
- [ ] Create git tag: `git tag v1.1.0`
- [ ] Push to GitHub: `git push origin v1.1.0`
- [ ] Create GitHub release dengan executable
- [ ] Send to users / upload to download server

## 🚀 Quick Start

### Untuk Development (Developers)

**First Time Setup** (5 menit)
```bash
# 1. Clone dan setup
git clone https://github.com/wahyudedik/pos-python.git
cd pos-python
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python scripts/init_db.py

# 4. Run aplikasi
python src/main.py
```

**Daily Development**
```bash
# Activate environment
.\.venv\Scripts\Activate.ps1

# Run aplikasi
python src/main.py

# Test code
pytest tests/ -v
```

### Untuk End Users (Non-Technical)

**First Time Use**
1. Download file: `POS-System.exe`
2. Double-click aplikasi
3. Database otomatis dibuat
4. Start selling!

**Daily Operation**
1. Double-click `POS-System.exe`
2. Login dengan user credentials
3. Start making sales
4. System auto-saves semua data

**Update to New Version**
1. Download file baru: `POS-System-v1.1.0.exe`
2. Stop aplikasi yang sedang running
3. Double-click file baru
4. Semua data (inventory, history) tetap ada

### Untuk Business User (Manager/Owner)

**Setup Initial**
1. Get file `POS-System.exe` dari admin/IT
2. Run aplikasi
3. Login dengan admin account
4. Setup toko di Settings → Store Settings
5. Add products di Inventory menu
6. Add payment methods di Settings → Payment Methods

**Daily Monitoring**
1. Check sales di Reports → Daily Sales
2. Monitor inventory di Inventory → Stock Status
3. Generate reports untuk owner/accounting

**System Maintenance**
1. Backup data: Settings → Backup Database (weekly)
2. Check logs: Check logs folder untuk troubleshooting
3. Update when available: Download new version from admin

---

### First Time Operation

#### Untuk Operator Kasir
1. Operator login & start selling
2. Scan barcode atau manual input SKU
3. Add quantity & apply discount jika ada
4. Select payment method
5. Process payment
6. Print receipt
7. System automatically update inventory

#### Untuk Manager
1. Check daily sales report
2. Monitor inventory levels
3. Generate reports untuk owner
4. Manage user accounts

#### Untuk Admin/IT
1. Setup sistem & database
2. Create user accounts
3. Configure payment methods
4. Setup printers & barcode scanners
5. Regular backups
6. Deploy updates

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

## 🆘 Troubleshooting & FAQ

### Development Issues

**Issue: "ModuleNotFoundError" saat run**
```bash
# Solution: Pastikan virtual environment activated
.\.venv\Scripts\Activate.ps1

# Check python path
python -c "import sys; print(sys.prefix)"
```

**Issue: Database not found**
```bash
# Solution: Initialize database
python scripts/init_db.py

# Check database file exists
ls pos.db
```

**Issue: PyInstaller not found**
```bash
# Solution: Install PyInstaller
pip install PyInstaller
```

### Runtime Issues

**Issue: Aplikasi crash saat startup**
```
Solution:
1. Check logs di logs/ folder
2. Check database permissions
3. Run as Administrator
4. Reinstall database: python scripts/init_db.py
```

**Issue: Barcode scanner not detecting**
```
Solution:
1. Check scanner is plugged in
2. Check hardware config di config/hardware.json
3. Update USB drivers
4. Test scanner di Settings → Detect Hardware
```

**Issue: Printer not printing**
```
Solution:
1. Check printer is powered on & connected
2. Check printer drivers installed
3. Test print di Settings → Test Printer
4. Check printer queue
```

### Build Issues

**Issue: Build takes too long**
```
Solution:
- First build: 15-20 minutes (normal, bundles Python)
- Use --onedir instead of --onefile for faster builds
- Use --exclude-module to skip unnecessary libraries
```

**Issue: Executable too large (250+ MB)**
```
Solution:
- This is normal for PyInstaller (includes Python runtime)
- Compress with ZIP for distribution: 250MB → 80MB compressed
```

---

## 📚 Documentation & Guides

- **User Guide**: [QUICKSTART.md](QUICKSTART.md) - How to use aplikasi
- **Developer Guide**: [Development setup dan workflow](#🚀-development-setup)
- **Installer Guide**: [INSTALLER_QUICKSTART.md](INSTALLER_QUICKSTART.md) - Build & distribute
- **Payment Integration**: [docs/PAYMENT_GATEWAY.md](docs/PAYMENT_GATEWAY.md)
- **API Documentation**: [docs/API.md](docs/API.md) (future)

---

## 🤝 Contributing

Berkontribusi untuk POS System:

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes & test
4. Commit: `git commit -m "Add amazing feature"`
5. Push: `git push origin feature/amazing-feature`
6. Open Pull Request

---

## 📞 Support & Contact

Untuk pertanyaan, bug reports, atau feature requests:

- **GitHub Issues**: [Create issue](https://github.com/wahyudedik/pos-python/issues)
- **Documentation**: Check [docs/](docs/) folder
- **Email**: support@pos-system.id (future)
- **Discussion**: [GitHub Discussions](https://github.com/wahyudedik/pos-python/discussions)

---

## 📄 License

MIT License - Feel free to use untuk personal & commercial projects

---

**Version:** 1.0.0-beta
**Status:** Under Development
**Last Updated:** Desember 2025
