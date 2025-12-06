"""
Reports Screen - Laporan Penjualan dan Analitik
Screen untuk melihat laporan penjualan, grafik, dan statistik
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QDateEdit, QPushButton, QComboBox, QHeaderView, QTabWidget, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from sqlalchemy import select, func
from datetime import datetime, timedelta
import logging

from src.config.database import get_session
from src.models.transaction import Transaction

logger = logging.getLogger(__name__)


class ReportsScreen(QWidget):
    """Screen untuk laporan dan analitik"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_reports()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Laporan Penjualan")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        
        # Date range
        date_label = QLabel("Periode:")
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setCalendarPopup(True)
        
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        
        filter_layout.addWidget(date_label)
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("sampai"))
        filter_layout.addWidget(self.date_to)
        
        # Report type
        report_label = QLabel("Tipe Laporan:")
        self.report_type = QComboBox()
        self.report_type.addItems(["Harian", "Mingguan", "Bulanan"])
        filter_layout.addWidget(report_label)
        filter_layout.addWidget(self.report_type)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_reports)
        filter_layout.addWidget(refresh_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Tabs for different reports
        self.tabs = QTabWidget()
        
        # Tab 1: Daily Sales
        self.daily_table = QTableWidget()
        self.daily_table.setColumnCount(6)
        self.daily_table.setHorizontalHeaderLabels([
            "Tanggal", "Jumlah Transaksi", "Total Penjualan", 
            "Total Diskon", "Pajak", "Pendapatan Bersih"
        ])
        self.daily_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.daily_table, "Penjualan Harian")
        
        # Tab 2: Payment Methods
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(4)
        self.payment_table.setHorizontalHeaderLabels([
            "Metode Pembayaran", "Jumlah Transaksi", "Total", "Persentase"
        ])
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.payment_table, "Metode Pembayaran")
        
        # Tab 3: Summary
        self.summary_widget = QWidget()
        self.summary_layout = QVBoxLayout()
        self.tabs.addTab(self.summary_widget, "Ringkasan")
        
        layout.addWidget(self.tabs)
        
        # Export button
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        
        export_pdf_btn = QPushButton("📄 Export PDF")
        export_pdf_btn.setMinimumHeight(40)
        export_pdf_btn.clicked.connect(self.export_pdf)
        
        export_excel_btn = QPushButton("📊 Export Excel")
        export_excel_btn.setMinimumHeight(40)
        export_excel_btn.clicked.connect(self.export_excel)
        
        print_btn = QPushButton("🖨 Print")
        print_btn.setMinimumHeight(40)
        print_btn.clicked.connect(self.print_report)
        
        export_layout.addWidget(export_pdf_btn)
        export_layout.addWidget(export_excel_btn)
        export_layout.addWidget(print_btn)
        
        layout.addLayout(export_layout)
        
        self.setLayout(layout)
    
    def load_reports(self):
        """Load reports data"""
        try:
            session = get_session()
            
            date_from = self.date_from.date().toPyDate()
            date_to = self.date_to.date().toPyDate()
            
            # Get transactions in date range
            stmt = select(Transaction).where(
                (Transaction.created_at >= date_from) &
                (Transaction.created_at <= date_to)
            )
            transactions = session.execute(stmt).scalars().all()
            
            # Daily summary
            daily_stats = {}
            for transaction in transactions:
                date_key = transaction.created_at.date()
                if date_key not in daily_stats:
                    daily_stats[date_key] = {
                        'count': 0,
                        'total': 0,
                        'discount': 0,
                        'tax': 0
                    }
                
                daily_stats[date_key]['count'] += 1
                daily_stats[date_key]['total'] += float(transaction.total)
                daily_stats[date_key]['discount'] += float(transaction.discount or 0)
                daily_stats[date_key]['tax'] += float(transaction.tax or 0)
            
            # Load daily table
            self.daily_table.setRowCount(len(daily_stats))
            total_sales = 0
            total_discount = 0
            total_tax = 0
            
            for row, (date, stats) in enumerate(sorted(daily_stats.items())):
                self.daily_table.setItem(row, 0, QTableWidgetItem(date.strftime("%d-%m-%Y")))
                self.daily_table.setItem(row, 1, QTableWidgetItem(str(stats['count'])))
                self.daily_table.setItem(row, 2, QTableWidgetItem(f"Rp {int(stats['total']):,}"))
                self.daily_table.setItem(row, 3, QTableWidgetItem(f"Rp {int(stats['discount']):,}"))
                self.daily_table.setItem(row, 4, QTableWidgetItem(f"Rp {int(stats['tax']):,}"))
                
                net = stats['total'] - stats['discount']
                self.daily_table.setItem(row, 5, QTableWidgetItem(f"Rp {int(net):,}"))
                
                total_sales += stats['total']
                total_discount += stats['discount']
                total_tax += stats['tax']
            
            # Payment methods
            payment_stats = {}
            for transaction in transactions:
                if transaction.payment_method not in payment_stats:
                    payment_stats[transaction.payment_method] = {'count': 0, 'total': 0}
                
                payment_stats[transaction.payment_method]['count'] += 1
                payment_stats[transaction.payment_method]['total'] += float(transaction.total)
            
            self.payment_table.setRowCount(len(payment_stats))
            for row, (method, stats) in enumerate(sorted(payment_stats.items())):
                percentage = (stats['total'] / total_sales * 100) if total_sales > 0 else 0
                
                self.payment_table.setItem(row, 0, QTableWidgetItem(method))
                self.payment_table.setItem(row, 1, QTableWidgetItem(str(stats['count'])))
                self.payment_table.setItem(row, 2, QTableWidgetItem(f"Rp {int(stats['total']):,}"))
                self.payment_table.setItem(row, 3, QTableWidgetItem(f"{percentage:.1f}%"))
            
            # Summary
            self.update_summary(
                len(transactions),
                total_sales,
                total_discount,
                total_tax,
                total_sales - total_discount
            )
            
            session.close()
            logger.info(f"Loaded reports for period {date_from} to {date_to}")
        except Exception as e:
            logger.error(f"Error loading reports: {e}")
    
    def update_summary(self, trans_count, total_sales, total_discount, total_tax, net_income):
        """Update summary tab"""
        # Clear previous layout
        while self.summary_layout.count():
            item = self.summary_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
        
        # Add summary labels
        summary_data = [
            ("Total Transaksi:", f"{trans_count}"),
            ("Total Penjualan:", f"Rp {int(total_sales):,}"),
            ("Total Diskon:", f"Rp {int(total_discount):,}"),
            ("Total Pajak:", f"Rp {int(total_tax):,}"),
            ("Pendapatan Bersih:", f"Rp {int(net_income):,}"),
        ]
        
        for label, value in summary_data:
            row_layout = QHBoxLayout()
            
            label_widget = QLabel(label)
            label_widget.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            
            value_widget = QLabel(value)
            value_widget.setFont(QFont("Arial", 12))
            value_widget.setStyleSheet("color: #2196F3; font-weight: bold;")
            
            row_layout.addWidget(label_widget)
            row_layout.addStretch()
            row_layout.addWidget(value_widget)
            
            self.summary_layout.addLayout(row_layout)
        
        self.summary_layout.addStretch()
    
    def export_pdf(self):
        """Export report as PDF"""
        try:
            from datetime import datetime
            date_from = self.date_from.date().toString()
            date_to = self.date_to.date().toString()
            
            filename = f"POS_Report_{date_from}_to_{date_to}.pdf"
            logger.info(f"Exporting report as PDF: {filename}")
            QMessageBox.information(
                self, "Sukses", 
                f"Report telah diproses untuk PDF export:\n{filename}\n\nFitur PDF akan diimplementasikan dengan library ReportLab."
            )
        except Exception as e:
            logger.error(f"Error in export_pdf: {e}")
            QMessageBox.critical(self, "Error", f"Gagal export PDF: {str(e)}")
    
    def export_excel(self):
        """Export report as Excel"""
        try:
            from datetime import datetime
            import csv
            from pathlib import Path
            
            date_from = self.date_from.date().toString()
            date_to = self.date_to.date().toString()
            
            filename = f"POS_Report_{date_from}_to_{date_to}.csv"
            
            # Create exports directory if it doesn't exist
            export_dir = Path("exports")
            export_dir.mkdir(exist_ok=True)
            filepath = export_dir / filename
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(["LAPORAN PENJUALAN POS"])
                writer.writerow([f"Periode: {date_from} s/d {date_to}"])
                writer.writerow([])
                
                # Write daily sales data
                writer.writerow(["PENJUALAN HARIAN"])
                writer.writerow(["Tanggal", "Transaksi", "Penjualan", "Diskon", "Pajak", "Bersih"])
                
                for row in range(self.daily_table.rowCount()):
                    row_data = []
                    for col in range(self.daily_table.columnCount()):
                        item = self.daily_table.item(row, col)
                        if item:
                            row_data.append(item.text())
                    if row_data:
                        writer.writerow(row_data)
                
                writer.writerow([])
                
                # Write payment methods
                writer.writerow(["METODE PEMBAYARAN"])
                writer.writerow(["Metode", "Transaksi", "Total", "Persentase"])
                
                for row in range(self.payment_table.rowCount()):
                    row_data = []
                    for col in range(self.payment_table.columnCount()):
                        item = self.payment_table.item(row, col)
                        if item:
                            row_data.append(item.text())
                    if row_data:
                        writer.writerow(row_data)
                
                # Write summary
                writer.writerow([])
                writer.writerow(["RINGKASAN"])
                # Write summary information if available
                writer.writerow(["Total Transaksi: Check Reports tab"])
                writer.writerow(["Total Penjualan: Check Reports tab"])
                writer.writerow(["Total Diskon: Check Reports tab"])
                writer.writerow(["Total Pajak: Check Reports tab"])
            
            logger.info(f"Report exported to: {filepath}")
            QMessageBox.information(
                self, "Sukses",
                f"Report telah diekspor ke:\n{filepath}"
            )
        except Exception as e:
            logger.error(f"Error in export_excel: {e}")
            QMessageBox.critical(self, "Error", f"Gagal export Excel: {str(e)}")
    
    def print_report(self):
        """Print report"""
        try:
            logger.info("Print report requested")
            QMessageBox.information(
                self, "Print Report",
                "Fitur print akan mengirim laporan ke printer Anda.\n\n"
                "Silakan gunakan fungsi Export terlebih dahulu, "
                "kemudian buka file dengan aplikasi untuk mencetak."
            )
        except Exception as e:
            logger.error(f"Error in print_report: {e}")
            QMessageBox.critical(self, "Error", f"Gagal print report: {str(e)}")
