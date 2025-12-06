# Panduan Membuat dan Menggunakan Installer POS System

## 📦 Overview

Aplikasi POS Offline System dapat didistribusikan dengan 2 cara:

1. **Standalone Executable** - File .exe tunggal yang bisa langsung dijalankan
2. **NSIS Installer** - Installer profesional seperti aplikasi Windows biasa

---

## 🚀 Cara Membuat Installer

### Metode 1: Menggunakan PowerShell (Recommended)

```powershell
# Buka PowerShell dari folder project
cd D:\PROJECT\PYTHON\pos

# Jalankan script builder
.\build_installer.ps1
```

**Opsi tambahan:**
```powershell
# Clean build (menghapus build lama)
.\build_installer.ps1 -CleanBuild

# Hanya buat executable (skip NSIS)
.\build_installer.ps1 -BuildType exe

# Skip NSIS jika tidak terinstall
.\build_installer.ps1 -SkipNSIS
```

### Metode 2: Menggunakan Batch Script

```batch
cd D:\PROJECT\PYTHON\pos
build_installer.bat
```

### Metode 3: Manual dengan PyInstaller

```bash
# Install PyInstaller
pip install PyInstaller

# Build executable
pyinstaller pos_system.spec --distpath=dist --buildpath=build -y
```

---

## 📋 Prerequisites untuk Build

### Requirement Minimum
- **Python** 3.10 atau lebih tinggi
- **pip** (Python Package Manager)
- **PyInstaller** (akan diinstall otomatis)

### Untuk NSIS Installer (Optional)
- **NSIS 3.0+** - Download dari https://nsis.sourceforge.io
- Pilih "NSIS 3.x" → Download installer
- Jalankan installer dengan default settings

**Verifikasi NSIS installed:**
```powershell
Get-Command makensis
# atau
dir "C:\Program Files\NSIS\makensis.exe"
```

---

## 📂 Output File Structure

Setelah build selesai:

```
dist/
├── POS-System/                          # Standalone aplikasi
│   ├── POS-System.exe                   # Main executable
│   ├── _internal/                       # Dependencies
│   ├── base_library.zip
│   └── ...
│
└── POS-System-Installer-v1.0.0.exe     # NSIS installer (jika NSIS installed)
```

---

## 💾 Distribusi ke User

### Cara 1: Standalone Folder (Paling Sederhana)

```
1. Buka: dist\POS-System
2. Compress sebagai ZIP atau RAR
3. Kirim ke user
4. User extract dan double-click POS-System.exe
```

**Kelebihan:**
- Tidak perlu admin rights
- Tidak perlu install
- Bisa langsung run

**Kekurangan:**
- Folder cukup besar (~200-300 MB)
- User harus manual click .exe

### Cara 2: NSIS Installer (Professional)

```
1. Gunakan: dist\POS-System-Installer-v1.0.0.exe
2. Kirim ke user
3. User double-click dan ikuti wizard
```

**Kelebihan:**
- Terlihat profesional
- Instalasi otomatis ke Program Files
- Shortcuts di Desktop dan Start Menu
- Registry entries untuk uninstall

**Kekurangan:**
- Memerlukan NSIS untuk build
- Installer ~150-200 MB (masih besar)

---

## 🔧 File Konfigurasi Installer

### setup.py
Entry point untuk setuptools (optional, untuk pip install)

```python
python -m pip install -e .
```

### pos_system.spec
File konfigurasi PyInstaller

**Opsi penting:**
- `console=False` - Sembunyikan console window
- `icon=...` - Path ke icon file
- `hiddenimports` - Module yang dimuat dynamic

### POS-System-Installer.nsi
Script NSIS untuk installer

**Customize:**
- Path file
- Company name
- Version number
- License file

---

## 🎨 Customization

### 1. Ganti Icon Aplikasi

Letakkan file icon di: `src/assets/icon.ico`

```python
# Di pos_system.spec:
icon=str(project_root / 'src' / 'assets' / 'icon.ico')
```

**Buat Icon dari PNG:**
```bash
pip install pillow
python -c "from PIL import Image; img = Image.open('logo.png'); img.save('icon.ico')"
```

### 2. Customize Installer Welcome Message

Edit: `installer/POS-System-Installer.nsi`

```nsi
; Ubah info installer
Name "POS Offline System v1.0.0"
InstallDir "$PROGRAMFILES\POS-System"
OutFile "dist\POS-System-Installer-v1.0.0.exe"
```

### 3. Add License File

1. Buat file: `LICENSE`
2. NSIS akan otomatis menampilkan halaman license

---

## ✅ Verification Checklist

Sebelum distribute:

- [ ] Test executable di fresh Windows install
- [ ] Database dibuat otomatis saat first run
- [ ] All features working (Sales, Inventory, Reports, Settings)
- [ ] Export functions working
- [ ] Backup/Restore working
- [ ] Error handling working
- [ ] Tidak ada error di console (jika console=True)

---

## 🐛 Troubleshooting

### PyInstaller tidak ditemukan
```powershell
python -m pip install PyInstaller
```

### NSIS tidak ditemukan
```powershell
# Download dan install dari: https://nsis.sourceforge.io
# Atau skip NSIS dan gunakan standalone executable
.\build_installer.ps1 -SkipNSIS
```

### Executable tidak bisa dijalankan
```bash
# Check anti-virus - mungkin block file
# Try run as Administrator
# Check Windows Defender Smart Screen settings
```

### Database permission denied
```bash
# Ensure folder writable:
# - C:\ProgramFiles\POS-System\data\
# - C:\ProgramFiles\POS-System\exports\
# - C:\ProgramFiles\POS-System\logs\
```

### ModuleNotFoundError saat run
```bash
# Add ke hiddenimports di pos_system.spec:
hiddenimports=['module_name', ...]
```

---

## 📊 Size Optimization

Ukuran file besar karena PyInstaller bundling Python runtime:

**Solusi:**
1. Exclude module yang tidak dipakai
2. Use UPX untuk compress executable (optional)
3. Consider using PyInstaller onefile mode

---

## 🔐 Code Signing (Optional)

Untuk aplikasi production, sign executable:

```powershell
# Windows Code Signing
signtool sign /f certificate.pfx /p password /t http://timestamp.server /fd SHA256 POS-System.exe
```

---

## 📝 Distribution Checklist

Sebelum kirim ke user, include:

- [ ] **POS-System-Installer-v1.0.0.exe** (Installer)
- [ ] **README.md** (Usage guide)
- [ ] **QUICKSTART.md** (Getting started)
- [ ] **.env.example** (Configuration template)
- [ ] **LICENSE** (License file)

---

## 🎯 Final Distribution Package

Folder struktur untuk distribution:

```
POS-System-v1.0.0/
├── POS-System-Installer-v1.0.0.exe
├── README.md
├── QUICKSTART.md
├── .env.example
├── LICENSE
└── INSTALLATION_GUIDE.md
```

---

## 📞 Support

**Jika ada masalah:**

1. Check logs di: `C:\ProgramFiles\POS-System\logs\app.log`
2. Run application dengan command line untuk lihat error:
   ```bash
   cd "C:\Program Files\POS-System"
   POS-System.exe
   ```
3. Report issue dengan log file

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-06  
**Status**: Ready for distribution
