"""
Sales Screen for Point of Sale
Main interface for cashiers to process sales with barcode scanner and payment integration
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDialog, QMessageBox,
    QTabWidget, QGroupBox, QGridLayout, QInputDialog, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread
from PyQt6.QtGui import QFont, QColor
from datetime import datetime
from typing import Optional, List, Dict
import logging

from src.config.settings import STORE_CURRENCY
from src.utils.currency import format_currency, calculate_change
from src.services.midtrans_gateway import MidtransGateway
from src.exceptions.custom_exceptions import PaymentException, InsufficientStockException
from src.config.database import get_session
from src.models.product import Product
from src.models.transaction import Transaction
from sqlalchemy import select, or_

logger = logging.getLogger(__name__)


class SalesScreen(QWidget):
    """Point of Sale sales screen with shopping cart and payment processing"""
    
    def __init__(self, parent=None):
        """Initialize sales screen"""
        super().__init__(parent)
        self.cart_items: List[Dict] = []
        self.payment_gateway: Optional[MidtransGateway] = None
        self.current_product: Optional[Product] = None
        self.init_ui()
        self.setup_scanner()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QHBoxLayout()
        
        # Left side: Product/Barcode Input
        left_panel = self.create_left_panel()
        layout.addWidget(left_panel, 1)
        
        # Right side: Cart and Totals
        right_panel = self.create_right_panel()
        layout.addWidget(right_panel, 1)
        
        self.setLayout(layout)
        self.setWindowTitle("Penjualan - POS System")
    
    def create_left_panel(self) -> QGroupBox:
        """Create left panel for product input"""
        group = QGroupBox("Input Produk")
        layout = QVBoxLayout()
        
        # Barcode input
        barcode_label = QLabel("Barcode/SKU:")
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Scan barcode atau masukkan SKU")
        self.barcode_input.returnPressed.connect(self.on_barcode_scanned)
        layout.addWidget(barcode_label)
        layout.addWidget(self.barcode_input)
        
        # Product info (read-only)
        product_label = QLabel("Produk:")
        self.product_display = QLineEdit()
        self.product_display.setReadOnly(True)
        layout.addWidget(product_label)
        layout.addWidget(self.product_display)
        
        # Price display
        price_label = QLabel("Harga:")
        self.price_display = QLineEdit()
        self.price_display.setReadOnly(True)
        layout.addWidget(price_label)
        layout.addWidget(self.price_display)
        
        # Quantity
        qty_label = QLabel("Jumlah:")
        qty_layout = QHBoxLayout()
        self.qty_spinbox = QSpinBox()
        self.qty_spinbox.setMinimum(1)
        self.qty_spinbox.setValue(1)
        qty_layout.addWidget(self.qty_spinbox)
        qty_layout.addStretch()
        layout.addWidget(qty_label)
        layout.addLayout(qty_layout)
        
        # Add to cart button
        add_button = QPushButton("Tambah ke Keranjang (Enter)")
        add_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        add_button.clicked.connect(self.add_to_cart)
        layout.addWidget(add_button)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def create_right_panel(self) -> QWidget:
        """Create right panel for cart and totals"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Cart table
        cart_label = QLabel("Keranjang Belanja")
        cart_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(cart_label)
        
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(
            ["Produk", "Qty", "Harga", "Total", "Hapus"]
        )
        self.cart_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.cart_table)
        
        # Totals section
        totals_group = self.create_totals_section()
        layout.addWidget(totals_group)
        
        # Payment buttons
        payment_layout = QHBoxLayout()
        
        cash_btn = QPushButton("Pembayaran Tunai (F3)")
        cash_btn.setStyleSheet("background-color: #2196F3; color: white;")
        cash_btn.clicked.connect(self.process_cash_payment)
        payment_layout.addWidget(cash_btn)
        
        card_btn = QPushButton("Pembayaran Kartu/E-wallet (F4)")
        card_btn.setStyleSheet("background-color: #FF9800; color: white;")
        card_btn.clicked.connect(self.process_card_payment)
        payment_layout.addWidget(card_btn)
        
        cancel_btn = QPushButton("Batal (Esc)")
        cancel_btn.setStyleSheet("background-color: #f44336; color: white;")
        cancel_btn.clicked.connect(self.clear_cart)
        payment_layout.addWidget(cancel_btn)
        
        layout.addLayout(payment_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_totals_section(self) -> QGroupBox:
        """Create totals display section"""
        group = QGroupBox("Ringkasan")
        layout = QGridLayout()
        
        # Subtotal
        layout.addWidget(QLabel("Subtotal:"), 0, 0)
        self.subtotal_label = QLabel(format_currency(0))
        self.subtotal_label.setFont(QFont("Arial", 11))
        layout.addWidget(self.subtotal_label, 0, 1)
        
        # Discount
        layout.addWidget(QLabel("Diskon:"), 1, 0)
        self.discount_label = QLabel(format_currency(0))
        self.discount_label.setFont(QFont("Arial", 11))
        layout.addWidget(self.discount_label, 1, 1)
        
        # Tax
        layout.addWidget(QLabel("PPN (10%):"), 2, 0)
        self.tax_label = QLabel(format_currency(0))
        self.tax_label.setFont(QFont("Arial", 11))
        layout.addWidget(self.tax_label, 2, 1)
        
        # Total
        total_font = QFont("Arial", 14, QFont.Weight.Bold)
        layout.addWidget(QLabel("TOTAL:"), 3, 0)
        self.total_label = QLabel(format_currency(0))
        self.total_label.setFont(total_font)
        self.total_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        layout.addWidget(self.total_label, 3, 1)
        
        group.setLayout(layout)
        return group
    
    def setup_scanner(self):
        """Setup barcode scanner (optional hardware integration)"""
        # This would connect to BarcodeScannerService if hardware available
        # For now, we accept manual input or scanning via keyboard
        pass
    
    def on_barcode_scanned(self):
        """Handle barcode scan input"""
        barcode = self.barcode_input.text().strip()
        if barcode:
            self.lookup_product(barcode)
    
    def lookup_product(self, barcode: str):
        """
        Lookup product by barcode/SKU from database
        
        Args:
            barcode: Product barcode or SKU
        """
        try:
            session = get_session()
            
            # Search by barcode or SKU
            stmt = select(Product).where(
                or_(
                    Product.barcode == barcode,
                    Product.sku == barcode
                )
            )
            product = session.execute(stmt).scalar_one_or_none()
            session.close()
            
            if product:
                self.product_display.setText(product.name)
                self.price_display.setText(format_currency(product.selling_price))
                self.current_product = product  # Store for later reference
                self.qty_spinbox.setValue(1)
                self.barcode_input.clear()
                self.qty_spinbox.setFocus()
            else:
                QMessageBox.warning(self, "Produk Tidak Ditemukan", 
                                  f"Barcode/SKU '{barcode}' tidak ditemukan")
                self.barcode_input.clear()
                self.barcode_input.setFocus()
        except Exception as e:
            logger.error(f"Error looking up product: {e}")
            QMessageBox.critical(self, "Error", f"Gagal mencari produk: {str(e)}")
            self.barcode_input.clear()
    
    def add_to_cart(self):
        """Add product to shopping cart"""
        product_name = self.product_display.text()
        if not product_name:
            QMessageBox.warning(self, "Error", "Pilih produk terlebih dahulu")
            return
        
        price_text = self.price_display.text()
        price = float(price_text.replace("Rp ", "").replace(".", "").replace(",", "."))
        qty = self.qty_spinbox.value()
        product_id = self.current_product.id if self.current_product else None
        
        # Check if product already in cart
        for item in self.cart_items:
            if item["name"] == product_name:
                item["qty"] += qty
                self.update_cart_display()
                self.product_display.clear()
                self.price_display.clear()
                self.barcode_input.setFocus()
                return
        
        # Add new item
        self.cart_items.append({
            "product_id": product_id,
            "name": product_name,
            "price": price,
            "qty": qty,
            "total": price * qty
        })
        
        self.update_cart_display()
        self.product_display.clear()
        self.price_display.clear()
        self.barcode_input.setFocus()
    
    def update_cart_display(self):
        """Update cart table and totals"""
        self.cart_table.setRowCount(len(self.cart_items))
        
        subtotal = 0
        for row, item in enumerate(self.cart_items):
            self.cart_table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(item["qty"])))
            self.cart_table.setItem(row, 2, QTableWidgetItem(format_currency(item["price"])))
            self.cart_table.setItem(row, 3, QTableWidgetItem(format_currency(item["total"])))
            
            # Delete button
            del_btn = QPushButton("X")
            del_btn.setStyleSheet("background-color: #f44336; color: white;")
            del_btn.clicked.connect(lambda checked, r=row: self.remove_from_cart(r))
            self.cart_table.setCellWidget(row, 4, del_btn)
            
            subtotal += item["total"]
        
        # Calculate totals
        tax = subtotal * 0.1
        discount = 0
        total = subtotal - discount + tax
        
        self.subtotal_label.setText(format_currency(subtotal))
        self.tax_label.setText(format_currency(tax))
        self.discount_label.setText(format_currency(discount))
        self.total_label.setText(format_currency(total))
    
    def remove_from_cart(self, row: int):
        """Remove item from cart"""
        if 0 <= row < len(self.cart_items):
            self.cart_items.pop(row)
            self.update_cart_display()
    
    def get_total(self) -> float:
        """Get total amount from display"""
        total_text = self.total_label.text()
        return float(total_text.replace("Rp ", "").replace(".", "").replace(",", "."))
    
    def process_cash_payment(self):
        """Process cash payment"""
        total = self.get_total()
        if total == 0:
            QMessageBox.warning(self, "Error", "Keranjang kosong")
            return
        
        # Input cash amount
        cash_input, ok = QInputDialog.getDouble(
            self, 
            "Pembayaran Tunai",
            f"Total: {format_currency(total)}\n\nJumlah uang tunai:",
            value=total,
            min=total
        )
        
        if ok:
            change = cash_input - total
            if change >= 0:
                QMessageBox.information(
                    self,
                    "Pembayaran Berhasil",
                    f"Jumlah: {format_currency(cash_input)}\n"
                    f"Kembalian: {format_currency(change)}"
                )
                self.print_receipt("Tunai", cash_input, change)
                self.clear_cart()
            else:
                QMessageBox.warning(self, "Error", "Uang tunai tidak cukup")
    
    def process_card_payment(self):
        """Process card/e-wallet payment"""
        total = self.get_total()
        if total == 0:
            QMessageBox.warning(self, "Error", "Keranjang kosong")
            return
        
        # Show payment method selection
        methods = ["Transfer Bank", "QRIS", "E-Wallet", "Kartu Kredit"]
        method, ok = self.get_payment_method(methods)
        
        if ok and method:
            QMessageBox.information(
                self,
                "Pembayaran Card/E-wallet",
                f"Metode: {method}\nTotal: {format_currency(total)}\n\n"
                "Proses pembayaran sedang dijalankan..."
            )
            self.print_receipt(method, total)
            self.clear_cart()
    
    def get_payment_method(self, methods: List[str]) -> tuple:
        """Show payment method dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Pilih Metode Pembayaran")
        layout = QVBoxLayout()
        
        combo = QComboBox()
        combo.addItems(methods)
        layout.addWidget(QLabel("Metode Pembayaran:"))
        layout.addWidget(combo)
        
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Batal")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return combo.currentText(), True
        return None, False
    
    def print_receipt(self, payment_method: str, amount_paid: float, change: float = 0):
        """
        Print receipt and save transaction to database
        
        Args:
            payment_method: Payment method name (Tunai, Transfer Bank, etc.)
            amount_paid: Amount paid by customer
            change: Change amount (for cash payments)
        """
        try:
            from datetime import datetime
            
            total = self.get_total()
            session = get_session()
            
            # Parse amounts from display labels
            subtotal_text = self.subtotal_label.text().replace("Rp ", "").replace(".", "").replace(",", ".")
            discount_text = self.discount_label.text().replace("Rp ", "").replace(".", "").replace(",", ".")
            tax_text = self.tax_label.text().replace("Rp ", "").replace(".", "").replace(",", ".")
            
            subtotal = float(subtotal_text) if subtotal_text else 0
            discount = float(discount_text) if discount_text else 0
            tax = float(tax_text) if tax_text else 0
            
            # Generate order ID
            order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create transaction
            transaction = Transaction(
                order_id=order_id,
                subtotal=subtotal,
                discount=discount,
                tax=tax,
                total=total,
                payment_method=payment_method,
                payment_status="completed",
                status="completed"
            )
            
            session.add(transaction)
            session.commit()
            transaction_id = transaction.id
            session.close()
            
            logger.info(f"Transaction saved - ID: {transaction_id}, Order: {order_id}, Method: {payment_method}, Total: {total}")
            
            # TODO: Integrate ThermalPrinterService here for actual receipt printing
        except Exception as e:
            logger.error(f"Error saving transaction: {e}")
            QMessageBox.critical(self, "Error", f"Gagal menyimpan transaksi: {str(e)}")
    
    def clear_cart(self):
        """Clear shopping cart"""
        self.cart_items.clear()
        self.update_cart_display()
        self.barcode_input.setFocus()
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key.Key_F3:
            self.process_cash_payment()
        elif event.key() == Qt.Key.Key_F4:
            self.process_card_payment()
        elif event.key() == Qt.Key.Key_Escape:
            self.clear_cart()
        else:
            super().keyPressEvent(event)
