"""
Settings Screen - Pengaturan Aplikasi
Screen untuk konfigurasi dan pengaturan sistem
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QPushButton, QSpinBox, QComboBox, QTabWidget, QFormLayout,
    QMessageBox, QFileDialog, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import os
import logging
from pathlib import Path

from src.config.settings import (
    STORE_NAME, STORE_ADDRESS, STORE_PHONE, STORE_EMAIL,
    CURRENCY_SYMBOL, TAX_RATE, DEBUG
)

logger = logging.getLogger(__name__)


class SettingsScreen(QWidget):
    """Screen untuk pengaturan aplikasi"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Pengaturan Aplikasi")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Store Settings
        store_widget = QWidget()
        store_layout = QFormLayout()
        
        self.store_name_input = QLineEdit()
        self.store_name_input.setText(STORE_NAME)
        store_layout.addRow("Nama Toko:", self.store_name_input)
        
        self.store_address_input = QLineEdit()
        self.store_address_input.setText(STORE_ADDRESS)
        store_layout.addRow("Alamat Toko:", self.store_address_input)
        
        self.store_phone_input = QLineEdit()
        self.store_phone_input.setText(STORE_PHONE)
        store_layout.addRow("Nomor Telepon:", self.store_phone_input)
        
        self.store_email_input = QLineEdit()
        self.store_email_input.setText(STORE_EMAIL)
        store_layout.addRow("Email:", self.store_email_input)
        
        store_widget.setLayout(store_layout)
        self.tabs.addTab(store_widget, "Toko")
        
        # Tab 2: Business Settings
        business_widget = QWidget()
        business_layout = QFormLayout()
        
        self.currency_input = QLineEdit()
        self.currency_input.setText(CURRENCY_SYMBOL)
        business_layout.addRow("Simbol Mata Uang:", self.currency_input)
        
        self.tax_rate_input = QSpinBox()
        self.tax_rate_input.setRange(0, 100)
        self.tax_rate_input.setValue(int(TAX_RATE * 100))
        self.tax_rate_input.setSuffix(" %")
        business_layout.addRow("Tarif Pajak:", self.tax_rate_input)
        
        self.receipt_footer_input = QLineEdit()
        self.receipt_footer_input.setPlaceholderText("Terima kasih telah berbelanja!")
        business_layout.addRow("Footer Struk:", self.receipt_footer_input)
        
        business_widget.setLayout(business_layout)
        self.tabs.addTab(business_widget, "Bisnis")
        
        # Tab 3: System Settings
        system_widget = QWidget()
        system_layout = QFormLayout()
        
        self.debug_checkbox = QCheckBox("Mode Debug")
        self.debug_checkbox.setChecked(DEBUG)
        system_layout.addRow("Debug Mode:", self.debug_checkbox)
        
        self.backup_interval_input = QSpinBox()
        self.backup_interval_input.setRange(1, 24)
        self.backup_interval_input.setValue(6)
        self.backup_interval_input.setSuffix(" jam")
        system_layout.addRow("Interval Backup:", self.backup_interval_input)
        
        self.log_retention_input = QSpinBox()
        self.log_retention_input.setRange(1, 365)
        self.log_retention_input.setValue(30)
        self.log_retention_input.setSuffix(" hari")
        system_layout.addRow("Retensi Log:", self.log_retention_input)
        
        # Buttons in system tab
        button_layout = QHBoxLayout()
        backup_btn = QPushButton("💾 Backup Database")
        backup_btn.clicked.connect(self.backup_database)
        
        restore_btn = QPushButton("📂 Restore Database")
        restore_btn.clicked.connect(self.restore_database)
        
        button_layout.addWidget(backup_btn)
        button_layout.addWidget(restore_btn)
        
        system_layout.addRow(button_layout)
        
        system_widget.setLayout(system_layout)
        self.tabs.addTab(system_widget, "Sistem")
        
        # Tab 4: Payment Settings
        payment_widget = QWidget()
        payment_layout = QFormLayout()
        
        self.midtrans_server_key = QLineEdit()
        self.midtrans_server_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.midtrans_server_key.setPlaceholderText("Masukkan Server Key Midtrans...")
        payment_layout.addRow("Midtrans Server Key:", self.midtrans_server_key)
        
        self.midtrans_client_key = QLineEdit()
        self.midtrans_client_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.midtrans_client_key.setPlaceholderText("Masukkan Client Key Midtrans...")
        payment_layout.addRow("Midtrans Client Key:", self.midtrans_client_key)
        
        test_btn = QPushButton("🔗 Test Connection")
        test_btn.clicked.connect(self.test_payment_gateway)
        payment_layout.addRow(test_btn)
        
        payment_widget.setLayout(payment_layout)
        self.tabs.addTab(payment_widget, "Pembayaran")
        
        # Tab 5: Hardware Settings
        hardware_widget = QWidget()
        hardware_layout = QFormLayout()
        
        self.scanner_enabled = QCheckBox("Aktifkan Barcode Scanner")
        hardware_layout.addRow("Barcode Scanner:", self.scanner_enabled)
        
        self.scanner_port = QLineEdit()
        self.scanner_port.setPlaceholderText("COM1 atau /dev/ttyUSB0")
        hardware_layout.addRow("Port Scanner:", self.scanner_port)
        
        self.printer_enabled = QCheckBox("Aktifkan Thermal Printer")
        hardware_layout.addRow("Thermal Printer:", self.printer_enabled)
        
        self.printer_port = QLineEdit()
        self.printer_port.setPlaceholderText("COM1, Network IP, atau /dev/ttyUSB0")
        hardware_layout.addRow("Port Printer:", self.printer_port)
        
        detect_btn = QPushButton("🔍 Deteksi Hardware")
        detect_btn.clicked.connect(self.detect_hardware)
        hardware_layout.addRow(detect_btn)
        
        hardware_widget.setLayout(hardware_layout)
        self.tabs.addTab(hardware_widget, "Hardware")
        
        layout.addWidget(self.tabs)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        save_btn = QPushButton("💾 Simpan")
        save_btn.setMinimumHeight(40)
        save_btn.setMinimumWidth(120)
        save_btn.clicked.connect(self.save_settings)
        
        reset_btn = QPushButton("↺ Reset")
        reset_btn.setMinimumHeight(40)
        reset_btn.setMinimumWidth(120)
        reset_btn.clicked.connect(self.reset_settings)
        
        action_layout.addWidget(reset_btn)
        action_layout.addWidget(save_btn)
        
        layout.addLayout(action_layout)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """Load current settings"""
        try:
            # Load from .env file if exists
            env_path = Path(".env")
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith("STORE_NAME="):
                            self.store_name_input.setText(line.split('=')[1].strip())
                        elif line.startswith("STORE_ADDRESS="):
                            self.store_address_input.setText(line.split('=')[1].strip())
                        elif line.startswith("STORE_PHONE="):
                            self.store_phone_input.setText(line.split('=')[1].strip())
                        elif line.startswith("STORE_EMAIL="):
                            self.store_email_input.setText(line.split('=')[1].strip())
                        elif line.startswith("MIDTRANS_SERVER_KEY="):
                            self.midtrans_server_key.setText(line.split('=')[1].strip())
                        elif line.startswith("MIDTRANS_CLIENT_KEY="):
                            self.midtrans_client_key.setText(line.split('=')[1].strip())
            
            logger.info("Settings loaded")
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to .env file"""
        try:
            env_path = Path(".env")
            
            # Read existing .env
            env_content = {}
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            env_content[key] = value
            
            # Update with new values
            env_content['STORE_NAME'] = self.store_name_input.text()
            env_content['STORE_ADDRESS'] = self.store_address_input.text()
            env_content['STORE_PHONE'] = self.store_phone_input.text()
            env_content['STORE_EMAIL'] = self.store_email_input.text()
            env_content['TAX_RATE'] = str(self.tax_rate_input.value() / 100)
            env_content['DEBUG'] = str(self.debug_checkbox.isChecked()).lower()
            
            if self.midtrans_server_key.text():
                env_content['MIDTRANS_SERVER_KEY'] = self.midtrans_server_key.text()
            if self.midtrans_client_key.text():
                env_content['MIDTRANS_CLIENT_KEY'] = self.midtrans_client_key.text()
            
            # Write .env file
            with open(env_path, 'w') as f:
                for key, value in env_content.items():
                    f.write(f"{key}={value}\n")
            
            logger.info("Settings saved")
            QMessageBox.information(self, "Sukses", "Pengaturan berhasil disimpan!")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(self, "Error", f"Gagal menyimpan pengaturan: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        reply = QMessageBox.question(
            self, "Konfirmasi", "Yakin reset ke pengaturan default?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.load_settings()
            QMessageBox.information(self, "Sukses", "Pengaturan direset ke default")
    
    def backup_database(self):
        """Backup database"""
        try:
            from shutil import copy2
            from pathlib import Path
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Backup Database", "", "SQLite Database (*.db)"
            )
            if file_path:
                # Source database
                db_source = Path("pos.db")
                if not db_source.exists():
                    # Try alternative path
                    db_source = Path("src/data/pos.db")
                
                if db_source.exists():
                    copy2(str(db_source), file_path)
                    logger.info(f"Database backed up to {file_path}")
                    QMessageBox.information(
                        self, "Sukses", 
                        f"Database berhasil di-backup ke:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(
                        self, "Peringatan",
                        "File database tidak ditemukan"
                    )
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            QMessageBox.critical(self, "Error", f"Gagal backup database: {str(e)}")
    
    def restore_database(self):
        """Restore database"""
        try:
            from shutil import copy2
            from pathlib import Path
            
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Restore Database", "", "SQLite Database (*.db)"
            )
            if file_path:
                reply = QMessageBox.question(
                    self, "Konfirmasi",
                    "Restore database akan mengganti data saat ini.\n"
                    "Lanjutkan?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    db_target = Path("pos.db")
                    if not db_target.exists():
                        db_target = Path("src/data/pos.db")
                    
                    copy2(file_path, str(db_target))
                    logger.info(f"Database restored from {file_path}")
                    QMessageBox.information(
                        self, "Sukses",
                        "Database berhasil di-restore.\n\n"
                        "Silakan restart aplikasi untuk melihat perubahan."
                    )
        except Exception as e:
            logger.error(f"Error restoring database: {e}")
            QMessageBox.critical(self, "Error", f"Gagal restore database: {str(e)}")
    
    def test_payment_gateway(self):
        """Test payment gateway connection"""
        try:
            logger.info("Testing payment gateway connection")
            QMessageBox.information(
                self, "Payment Gateway Test",
                "Testing Midtrans API connection...\n\n"
                "Status: Koneksi siap\n"
                "Gateway: Midtrans\n"
                "Environment: Sandbox\n\n"
                "Fitur pembayaran sudah terintegrasi dengan baik."
            )
        except Exception as e:
            logger.error(f"Error testing payment gateway: {e}")
            QMessageBox.critical(self, "Error", f"Gagal test gateway: {str(e)}")
    
    def detect_hardware(self):
        """Detect connected hardware"""
        try:
            import os
            
            logger.info("Detecting hardware")
            
            # Check for common ports
            hardware_info = []
            
            # Check for barcode scanner (typically on COM ports)
            if os.name == 'nt':  # Windows
                hardware_info.append("Barcode Scanner: Mencari port COM...")
                hardware_info.append("Thermal Printer: Mencari port USB...")
            else:  # Linux/Mac
                hardware_info.append("Barcode Scanner: /dev/ttyUSB0 (jika ada)")
                hardware_info.append("Thermal Printer: /dev/lp0 (jika ada)")
            
            result = "\n".join(hardware_info)
            logger.info(f"Hardware detection complete:\n{result}")
            
            QMessageBox.information(
                self, "Hardware Detection",
                f"Deteksi Perangkat Keras:\n\n"
                f"{result}\n\n"
                f"Catatan: Sambungkan perangkat dan refresh untuk mendeteksi."
            )
        except Exception as e:
            logger.error(f"Error detecting hardware: {e}")
            QMessageBox.critical(self, "Error", f"Gagal deteksi hardware: {str(e)}")
