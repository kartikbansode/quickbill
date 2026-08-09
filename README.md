<p align="center">
  <a href="https://github.com/kartikbansode/quickbill-customer-display-app">
    <img width="80" height="80" alt="logo" src="https://github.com/user-attachments/assets/cc80dfee-89d8-4fc7-905d-7dfbaa3b480b" />
  </a>
</p>

<h1 align="center">
  QuickBill
</h1>

<p align="center">
  <strong>Professional Desktop Billing & Inventory Management System</strong>
</p>

<p align="center">
  Fast billing · Barcode scanning · Inventory management · Payments · Invoices
</p>

<p align="center">
  <a href="https://github.com/kartikbansode/quickbill/releases">
    Releases
  </a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill/releases/download/v2.2.0/QuickBill_Setup_v2.2.0.exe">
    Download v2.2.0
  </a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill-customer-display-app">
    Customer Display App
  </a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill-barcode-scanner-app">
    Barcode Scanner App
  </a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill">
    Repository
  </a>
</p>

<p align="center">
  <img
    src="https://img.shields.io/badge/Version-2.2.0-blue"
    alt="Version 2.2.0"
  />
  <img
    src="https://img.shields.io/badge/Python-3.11%2B-yellow"
    alt="Python 3.11+"
  />
  <img
    src="https://img.shields.io/badge/Platform-Windows-blue"
    alt="Windows"
  />
  <img
    src="https://img.shields.io/badge/License-MIT-green"
    alt="MIT License"
  />
</p>

<p align="center">
  QuickBill is the core desktop billing application of the QuickBill ecosystem,
  built for retail shops and small businesses. It combines fast point-of-sale
  billing, barcode scanning, product and inventory management, payment
  processing, professional invoice generation, bill history, and local
  business data management in a single desktop application.
</p>



<p align="center">
  <strong>Part of the QuickBill Ecosystem</strong>
  <br>
  QuickBill Desktop is the core billing system and authoritative source
  for products, inventory, bills, payments and transactions.
</p>

<p align="center">
  <a href="https://github.com/kartikbansode/quickbill-customer-display-app">
    Customer Display
  </a>
  &nbsp;·&nbsp;
  Real-time customer-facing billing, payment, QR and transaction display
  <br>
  <a href="https://github.com/kartikbansode/quickbill-barcode-scanner-app">
    Barcode Scanner
  </a>
  &nbsp;·&nbsp;
  Companion Android barcode scanning application for QuickBill Desktop
</p>


## What's Changed in v2.2.0

- Refined and more professional payment dialog
- Fixed payment workflow bugs and improved transaction locking
- Added dynamic UPI QR support for faster payment collection
- Improved customer display synchronization with desktop billing
- Added automatic reconnect and more stable display connection handling
- Better handling for cash, UPI, card, and credit payment modes
- Improved success screen behavior after completed transactions
- General UI and stability improvements
- Updated versioning, installer metadata, and release packaging

---

## Features

- Product management: add, edit, delete, search
- Barcode scanner support with USB / IP camera
- Fast billing workflow
- Professional PDF invoice generation
- Barcode label PDF generation
- Hold and resume bills
- Bill history, search, and reprint
- Automatic bill number generation
- Inventory and stock management
- Settings for app and billing configuration
- Portable JSON-based local database
- Windows installer and uninstaller

---

## Screenshots

### Customer Billing Window

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/a7da29cc-d3e1-47d2-a949-7c3a4842206b" />

### Product Management

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/12a94658-4a30-4b03-986a-eeb3cc6795fb" />

### Invoice

### 80 mm -

<img width="347" height="826" alt="image" src="https://github.com/user-attachments/assets/5b73904e-bc3e-4373-9fc0-c13501e12a9d" />

### A4 -

<img width="671" height="842" alt="image" src="https://github.com/user-attachments/assets/b87f7430-563c-400b-b93d-4c637720cee1" />

---

## Requirements

- Python 3.11+
- Windows 10 / Windows 11

---

## Installation

Clone the repository:

```bash
git clone https://github.com/kartikbansode/quickbill.git
```

Go to the project directory:

```bash
cd quickbill
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

## Building the Executable

```bash
pyinstaller QuickBill.spec
```

The executable will be generated inside the `dist` folder.

---

## License

This project is licensed under the MIT License.

---

## Contact

**LinkedIn**  
https://www.linkedin.com/in/kartikbansode

**GitHub**  
https://github.com/kartikbansode
