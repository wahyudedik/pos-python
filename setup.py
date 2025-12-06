"""
Setup configuration for POS Offline System
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="POS-Offline-System",
    version="1.0.0",
    description="Sistem Point of Sale (POS) Offline untuk toko retail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Wahyu Dedik",
    author_email="wahyudedik@example.com",
    url="https://github.com/wahyudedik/pos-python",
    license="MIT",
    
    packages=find_packages(),
    
    python_requires=">=3.10",
    
    install_requires=[
        # Core Python & GUI
        "PyQt6==6.6.1",
        "PyQt6-Qt6==6.6.1",
        "PyQt6-sip==13.6.0",
        "qdarkstyle==3.2.3",
        
        # Database & ORM
        "SQLAlchemy==2.0.23",
        "alembic==1.12.1",
        
        # Payment Gateway
        "midtransclient==1.4.2",
        
        # Data Processing & Utilities
        "pandas==2.1.3",
        "numpy==1.24.3",
        "python-dateutil==2.8.2",
        "pytz==2023.3",
        "python-dotenv>=1.0.0",
        
        # Reporting & PDF
        "ReportLab==4.0.7",
        "PyPDF2==4.0.1",
        
        # Barcode & Hardware
        "python-barcode==0.15.1",
        "pyzbar==0.1.9",
        "Pillow==10.1.0",
        "pyusb==1.2.1",
        "python-escpos==3.0",
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "installer": [
            "PyInstaller>=5.0",
        ],
    },
    
    entry_points={
        "console_scripts": [
            "pos-system=src.main:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Point-Of-Sale",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    
    project_urls={
        "Bug Reports": "https://github.com/wahyudedik/pos-python/issues",
        "Source": "https://github.com/wahyudedik/pos-python",
    },
)
