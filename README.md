<p align="center">
  <a href="https://github.com/kartikbansode/quickbill">
    <img width="80" height="80" alt="QuickBill logo" src="https://github.com/user-attachments/assets/cc80dfee-89d8-4fc7-905d-7dfbaa3b480b" />
  </a>
</p>

<h1 align="center">
  QuickBill
</h1>

<p align="center">
  <strong>Professional Desktop Billing & POS Management System</strong>
</p>

<p align="center">
  Fast billing · Barcode scanning · Product management · Payments · Invoices
</p>

<p align="center">
  <a href="https://github.com/kartikbansode/quickbill/releases">
    Releases
  </a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill/releases/tag/v3.0.0">
    v3.0.0
  </a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill-customer-display-app">
    Customer Display
  </a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill-barcode-scanner-app">
    Barcode Scanner
  </a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill">
    Repository
  </a>
</p>

<p align="center">
  <a href="https://github.com/kartikbansode/quickbill/releases">
    <img
      src="https://img.shields.io/badge/Version-3.0.0-blue"
      alt="Version 3.0.0"
    />
  </a>

  <a href="https://www.python.org/downloads/">
    <img
      src="https://img.shields.io/badge/Python-3.11%2B-yellow"
      alt="Python 3.11+"
    />
  </a>

  <a href="https://www.microsoft.com/en-us/windows">
    <img
      src="https://img.shields.io/badge/Platform-Windows-blue"
      alt="Windows"
    />
  </a>

  <a href="https://github.com/kartikbansode/quickbill/blob/main/LICENSE">
    <img
      src="https://img.shields.io/badge/License-Proprietary-green"
      alt="Proprietary License"
    />
  </a>
</p>

<p align="center">
  QuickBill is a professional desktop billing and point-of-sale system
  designed for retail shops and small businesses. It provides a complete
  billing workflow with barcode scanning, product management, inventory
  handling, payments, customer-facing display synchronization, invoice
  generation, and billing history.
</p>

---

## v3.0.0 — First Stable Release

QuickBill v3.0.0 marks the **first stable release** of the QuickBill desktop application.

This release consolidates the core billing, product management, invoice, payment, customer display, and POS functionality into a stable desktop application with a consistent professional interface and production-focused architecture.

### Release Highlights

- Stable QuickBill Pro desktop billing application
- Professional POS-oriented billing interface
- Improved application startup and splash screen workflow
- Consistent application-wide UI components and styling
- Barcode scanning and manual item entry
- Product and inventory management
- Professional invoice generation
- Bill history and reprinting
- Hold and resume billing workflow
- Multiple payment modes
- Dynamic UPI QR payment support
- Real-time customer display integration
- Improved customer display synchronization and reconnect handling
- Improved error handling and application stability
- Responsive desktop UI for different screen sizes
- Updated release documentation and project structure
- Versioned as the first stable `v3.0.0` release

---

## QuickBill Ecosystem

QuickBill Desktop is the **core billing application and authoritative source of billing data**.

It manages:

- Products
- Inventory
- Cart state
- Bills
- Transactions
- Payment state
- Customer information
- Invoice generation

The companion applications connect to QuickBill Desktop to provide additional POS functionality.

### Customer Display

:contentReference[oaicite:0]{index=0}

Provides a real-time customer-facing display for:

- Current bill items
- Quantities
- Prices
- Bill totals
- Payment information
- UPI QR display
- Payment success state

### Barcode Scanner

:contentReference[oaicite:1]{index=1}

Provides companion barcode-scanning functionality for QuickBill Desktop.

---

## Core Features

### Billing & POS

- Fast point-of-sale billing workflow
- Manual item entry
- Barcode-based item entry
- Automatic quantity handling
- Item-level quantity controls
- Item deletion
- Automatic subtotal and total calculation
- Tax and discount handling
- Automatic bill numbering
- Customer information capture
- Bill confirmation workflow
- Hold and resume bills

### Product Management

- Add products
- Edit products
- Delete products
- Search products
- Barcode-based product identification
- Product pricing
- Inventory and stock management

### Barcode Scanning

- USB barcode scanner support
- IP/webcam-based scanning support
- Continuous scanning
- Duplicate barcode handling
- Automatic product lookup
- Manual barcode entry

### Payments

Supported payment workflows include:

- Cash
- UPI
- Card
- Credit

Features include:

- Dynamic UPI QR generation
- Bill amount linked to payment QR
- Payment confirmation workflow
- Customer display payment state
- Transaction completion handling

### Invoice Generation

- Professional PDF invoices
- A4 invoice format
- 80 mm receipt format
- Printable billing documents
- Bill reprinting
- Automatic bill numbering

### Billing History

- View previous bills
- Search billing records
- Review transaction information
- Reprint invoices

### Customer Display

- Real-time bill synchronization
- Customer-facing item display
- Live totals
- Payment QR display
- Payment status
- Success screen
- Automatic reconnection
- Graceful disconnected state

---

## Screenshots

### Main Billing Window

<img width="1919" height="1079" alt="QuickBill Pro Billing Window" src="https://github.com/user-attachments/assets/a7da29cc-d3e1-47d2-a949-7c3a4842206b" />

### Product Management

<img width="1919" height="1079" alt="QuickBill Pro Product Management" src="https://github.com/user-attachments/assets/12a94658-4a30-4b03-986a-eeb3cc6795fb" />

### Invoice — 80 mm

<img width="347" height="826" alt="QuickBill Pro 80mm Invoice" src="https://github.com/user-attachments/assets/5b73904e-bc3e-4373-9fc0-c13501e12a9d" />

### Invoice — A4

<img width="671" height="842" alt="QuickBill Pro A4 Invoice" src="https://github.com/user-attachments/assets/b87f7430-563c-400b-b93d-4c637720cee1" />

---

## Technology Stack

| Component | Technology |
|---|---|
| Desktop Application | Python |
| GUI | Tkinter |
| Runtime | Python 3.11+ |
| Invoice Generation | PDF generation |
| Product/Billing Data | Local application storage |
| Barcode Scanning | USB / Camera / Companion Scanner |
| Customer Display | Network communication |
| Platform | Windows 10 / Windows 11 |
| Packaging | PyInstaller |

---

## Requirements

- Windows 10 or Windows 11
- Python 3.11 or newer
- Required Python packages listed in `requirements.txt`

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

This project is proprietary software.

Copyright © 2026 Kartik Bansode. All Rights Reserved.

The source code is publicly available for viewing, educational, portfolio, and evaluation purposes only.

No permission is granted to copy, reproduce, modify, redistribute, republish, commercially use, sublicense, sell, or create derivative works from this software or its source code without prior written permission from the copyright holder.

For complete terms and restrictions, see the [LICENSE](https://github.com/kartikbansode/quickbill/blob/main/LICENSE) file.

---

## Contact

**LinkedIn**  
https://www.linkedin.com/in/kartikbansode

**GitHub**  
https://github.com/kartikbansode
