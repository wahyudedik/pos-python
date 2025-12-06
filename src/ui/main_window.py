"""
Main Application Window
Central window for POS system dengan navigasi antar screens
"""

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import logging

from src.ui.screens.sales_screen import SalesScreen
from src.ui.screens.inventory_screen import InventoryScreen
from src.ui.screens.reports_screen import ReportsScreen
from src.ui.screens.settings_screen import SettingsScreen

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        self.setWindowTitle("POS Offline System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create stacked widget for screen navigation
        self.stacked_widget = QStackedWidget()
        self.screens = {}
        
        self.init_screens()
        self.init_ui()
    
    def init_screens(self):
        """Initialize all screen components"""
        # Sales screen
        self.screens['sales'] = SalesScreen()
        self.stacked_widget.addWidget(self.screens['sales'])
        
        # Inventory screen
        self.screens['inventory'] = InventoryScreen()
        self.stacked_widget.addWidget(self.screens['inventory'])
        
        # Reports screen
        self.screens['reports'] = ReportsScreen()
        self.stacked_widget.addWidget(self.screens['reports'])
        
        # Settings screen
        self.screens['settings'] = SettingsScreen()
        self.stacked_widget.addWidget(self.screens['settings'])
    
    def init_ui(self):
        """Initialize main UI"""
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Welcome message and navigation
        header_layout = QHBoxLayout()
        
        welcome = QLabel("POS Offline System")
        welcome.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(welcome)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Navigation buttons
        buttons_layout = QHBoxLayout()
        
        buttons = [
            ("Penjualan (F1)", "sales"),
            ("Inventaris (F2)", "inventory"),
            ("Laporan (F3)", "reports"),
            ("Pengaturan (F4)", "settings"),
        ]
        
        for label, screen_id in buttons:
            btn = QPushButton(label)
            btn.setMinimumHeight(50)
            btn.setFont(QFont("Arial", 11))
            btn.clicked.connect(lambda checked, s=screen_id: self.switch_screen(s))
            
            # Set button colors
            if screen_id == "sales":
                btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
            else:
                btn.setStyleSheet("background-color: #2196F3; color: white;")
            
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        
        # Add stacked widget for screens
        layout.addWidget(self.stacked_widget)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Show sales screen by default
        self.switch_screen('sales')
    
    def switch_screen(self, screen_id: str):
        """Switch to specified screen"""
        if screen_id in self.screens:
            self.stacked_widget.setCurrentWidget(self.screens[screen_id])
            logger.info(f"Switched to {screen_id} screen")
    
    def keyPressEvent(self, event):
        """Handle global keyboard shortcuts"""
        if event.key() == Qt.Key.Key_F1:
            self.switch_screen('sales')
        elif event.key() == Qt.Key.Key_F2:
            self.switch_screen('inventory')
        elif event.key() == Qt.Key.Key_F3:
            self.switch_screen('reports')
        elif event.key() == Qt.Key.Key_F4:
            self.switch_screen('settings')
        else:
            super().keyPressEvent(event)
