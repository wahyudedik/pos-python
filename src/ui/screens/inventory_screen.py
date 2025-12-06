"""
Inventory Screen - Manajemen Stok Produk
Screens untuk mengelola inventori produk
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QSpinBox, QComboBox, QDialog,
    QFormLayout, QMessageBox, QHeaderView
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal
from sqlalchemy import select
import logging

from src.config.database import get_session
from src.models.product import Product

logger = logging.getLogger(__name__)


class AddProductDialog(QDialog):
    """Dialog untuk menambah/edit produk"""
    
    product_saved = pyqtSignal(dict)
    
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle("Tambah/Edit Produk" if not product else "Edit Produk")
        self.setGeometry(200, 200, 500, 400)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI"""
        layout = QFormLayout()
        
        # Product name
        self.name_input = QLineEdit()
        if self.product:
            self.name_input.setText(self.product.name)
        layout.addRow("Nama Produk:", self.name_input)
        
        # SKU
        self.sku_input = QLineEdit()
        if self.product:
            self.sku_input.setText(self.product.sku)
        layout.addRow("SKU:", self.sku_input)
        
        # Barcode
        self.barcode_input = QLineEdit()
        if self.product:
            self.barcode_input.setText(self.product.barcode or "")
        layout.addRow("Barcode:", self.barcode_input)
        
        # Cost price
        self.cost_price_input = QSpinBox()
        self.cost_price_input.setRange(0, 999999999)
        if self.product:
            self.cost_price_input.setValue(int(self.product.cost_price))
        layout.addRow("Harga Modal (Rp):", self.cost_price_input)
        
        # Selling price
        self.selling_price_input = QSpinBox()
        self.selling_price_input.setRange(0, 999999999)
        if self.product:
            self.selling_price_input.setValue(int(self.product.selling_price))
        layout.addRow("Harga Jual (Rp):", self.selling_price_input)
        
        # Stock quantity
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 999999)
        if self.product:
            self.stock_input.setValue(int(self.product.quantity))
        layout.addRow("Stok:", self.stock_input)
        
        # Min stock
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setRange(0, 999999)
        if self.product:
            self.min_stock_input.setValue(int(self.product.min_quantity))
        layout.addRow("Minimum Stok:", self.min_stock_input)
        
        # Category
        self.category_input = QComboBox()
        self.category_input.addItems(["Electronics", "Beverages", "Food", "Clothing", "Other"])
        if self.product:
            index = self.category_input.findText(self.product.category)
            if index >= 0:
                self.category_input.setCurrentIndex(index)
        layout.addRow("Kategori:", self.category_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Simpan")
        cancel_btn = QPushButton("Batal")
        
        save_btn.clicked.connect(self.save_product)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
    
    def save_product(self):
        """Save product data"""
        try:
            if not self.name_input.text():
                QMessageBox.warning(self, "Validasi", "Nama produk tidak boleh kosong!")
                return
            
            product_data = {
                'name': self.name_input.text(),
                'sku': self.sku_input.text(),
                'barcode': self.barcode_input.text(),
                'cost_price': self.cost_price_input.value(),
                'selling_price': self.selling_price_input.value(),
                'quantity': self.stock_input.value(),
                'min_quantity': self.min_stock_input.value(),
                'category': self.category_input.currentText(),
            }
            
            self.product_saved.emit(product_data)
            self.accept()
        except Exception as e:
            logger.error(f"Error saving product: {e}")
            QMessageBox.critical(self, "Error", f"Gagal menyimpan produk: {str(e)}")


class InventoryScreen(QWidget):
    """Screen untuk manajemen inventori"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_products()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Manajemen Inventori")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Search and filter
        search_layout = QHBoxLayout()
        
        search_label = QLabel("Cari Produk:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nama, SKU, atau Barcode...")
        self.search_input.textChanged.connect(self.filter_products)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # Products table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nama", "SKU", "Barcode", "Harga Modal", 
            "Harga Jual", "Stok", "Min Stok", "Kategori"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("+ Tambah Produk")
        add_btn.setMinimumHeight(40)
        add_btn.clicked.connect(self.add_product)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✎ Edit")
        edit_btn.setMinimumHeight(40)
        edit_btn.clicked.connect(self.edit_product)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("✕ Hapus")
        delete_btn.setMinimumHeight(40)
        delete_btn.setStyleSheet("background-color: #f44336; color: white;")
        delete_btn.clicked.connect(self.delete_product)
        button_layout.addWidget(delete_btn)
        
        restock_btn = QPushButton("📦 Restock")
        restock_btn.setMinimumHeight(40)
        restock_btn.clicked.connect(self.restock_product)
        button_layout.addWidget(restock_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_products(self):
        """Load products from database"""
        try:
            session = get_session()
            stmt = select(Product)
            products = session.execute(stmt).scalars().all()
            
            self.table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                self.table.setItem(row, 0, QTableWidgetItem(str(product.id)))
                self.table.setItem(row, 1, QTableWidgetItem(product.name))
                self.table.setItem(row, 2, QTableWidgetItem(product.sku))
                self.table.setItem(row, 3, QTableWidgetItem(product.barcode or "-"))
                self.table.setItem(row, 4, QTableWidgetItem(f"Rp {int(product.cost_price):,}"))
                self.table.setItem(row, 5, QTableWidgetItem(f"Rp {int(product.selling_price):,}"))
                self.table.setItem(row, 6, QTableWidgetItem(str(int(product.quantity))))
                self.table.setItem(row, 7, QTableWidgetItem(str(int(product.min_quantity))))
                self.table.setItem(row, 8, QTableWidgetItem(product.category or "-"))
            
            session.close()
            logger.info(f"Loaded {len(products)} products")
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            QMessageBox.critical(self, "Error", f"Gagal memuat produk: {str(e)}")
    
    def filter_products(self):
        """Filter products by search term"""
        search_term = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            match = False
            for col in range(1, 4):  # Name, SKU, Barcode columns
                if search_term in self.table.item(row, col).text().lower():
                    match = True
                    break
            
            self.table.setRowHidden(row, not match)
    
    def add_product(self):
        """Add new product"""
        dialog = AddProductDialog(self)
        dialog.product_saved.connect(self.save_product_to_db)
        dialog.exec()
    
    def edit_product(self):
        """Edit selected product"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih produk untuk diedit!")
            return
        
        # Load product from database
        try:
            product_id = int(self.table.item(current_row, 0).text())
            session = get_session()
            product = session.query(Product).filter(Product.id == product_id).first()
            session.close()
            
            if product:
                dialog = AddProductDialog(self, product)
                dialog.product_saved.connect(self.save_product_to_db)
                dialog.exec()
        except Exception as e:
            logger.error(f"Error editing product: {e}")
            QMessageBox.critical(self, "Error", f"Gagal mengedit produk: {str(e)}")
    
    def delete_product(self):
        """Delete selected product"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih produk untuk dihapus!")
            return
        
        reply = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus produk ini?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                product_id = int(self.table.item(current_row, 0).text())
                session = get_session()
                product = session.query(Product).filter(Product.id == product_id).first()
                if product:
                    session.delete(product)
                    session.commit()
                    logger.info(f"Deleted product: {product.name}")
                session.close()
                self.load_products()
            except Exception as e:
                logger.error(f"Error deleting product: {e}")
                QMessageBox.critical(self, "Error", f"Gagal menghapus produk: {str(e)}")
    
    def restock_product(self):
        """Restock selected product"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih produk untuk di-restock!")
            return
        
        try:
            product_id = int(self.table.item(current_row, 0).text())
            session = get_session()
            product = session.query(Product).filter(Product.id == product_id).first()
            
            if product:
                # Simple restock dialog
                dialog = QDialog(self)
                dialog.setWindowTitle(f"Restock - {product.name}")
                dialog.setGeometry(300, 300, 300, 150)
                
                layout = QFormLayout()
                qty_input = QSpinBox()
                qty_input.setRange(1, 999999)
                layout.addRow("Jumlah Restock:", qty_input)
                
                btn_layout = QHBoxLayout()
                ok_btn = QPushButton("OK")
                cancel_btn = QPushButton("Batal")
                
                def save_restock():
                    new_qty = qty_input.value()
                    product.quantity += new_qty
                    session.commit()
                    logger.info(f"Restocked {product.name}: +{new_qty}")
                    self.load_products()
                    dialog.accept()
                
                ok_btn.clicked.connect(save_restock)
                cancel_btn.clicked.connect(dialog.reject)
                
                btn_layout.addWidget(ok_btn)
                btn_layout.addWidget(cancel_btn)
                layout.addRow(btn_layout)
                
                dialog.setLayout(layout)
                dialog.exec()
            
            session.close()
        except Exception as e:
            logger.error(f"Error restocking product: {e}")
            QMessageBox.critical(self, "Error", f"Gagal restock produk: {str(e)}")
    
    def save_product_to_db(self, product_data):
        """Save product to database"""
        try:
            session = get_session()
            
            # Check if product exists
            existing = session.query(Product).filter(
                Product.sku == product_data['sku']
            ).first()
            
            if existing:
                # Update
                existing.name = product_data['name']
                existing.barcode = product_data['barcode']
                existing.cost_price = product_data['cost_price']
                existing.selling_price = product_data['selling_price']
                existing.quantity = product_data['quantity']
                existing.min_quantity = product_data['min_quantity']
                existing.category = product_data['category']
            else:
                # Create new
                product = Product(
                    name=product_data['name'],
                    sku=product_data['sku'],
                    barcode=product_data['barcode'],
                    cost_price=product_data['cost_price'],
                    selling_price=product_data['selling_price'],
                    quantity=product_data['quantity'],
                    min_quantity=product_data['min_quantity'],
                    category=product_data['category']
                )
                session.add(product)
            
            session.commit()
            session.close()
            logger.info(f"Saved product: {product_data['name']}")
            self.load_products()
            QMessageBox.information(self, "Sukses", "Produk berhasil disimpan!")
        except Exception as e:
            logger.error(f"Error saving product to DB: {e}")
            QMessageBox.critical(self, "Error", f"Gagal menyimpan produk: {str(e)}")
