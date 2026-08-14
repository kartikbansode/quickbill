<p align="center">
  <a href="https://quickbill.kartikbansode.dev/">
    <img
      width="80"
      height="80"
      alt="QuickBill Logo"
      src="https://github.com/user-attachments/assets/cc80dfee-89d8-4fc7-905d-7dfbaa3b480b"
    />
  </a>
</p>

<h1 align="center">
  QuickBill
</h1>

<p align="center">
  <strong>Professional Desktop Billing & POS Management System</strong>
</p>

<p align="center">
  Fast billing · Barcode scanning · Inventory · Payments · Invoices
</p>

<p align="center">
  <a href="https://github.com/kartikbansode/quickbill/releases">Releases</a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill/releases/latest">Latest Release</a>
  &bull;
  <a href="https://quickbill.kartikbansode.dev/">Website</a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill-customer-display-app">Customer Display</a>
  &bull;
  <a href="https://github.com/kartikbansode/quickbill-barcode-scanner-app">Barcode Scanner</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.1.0 (Stable)-blue" alt="Version 3.1.0 (Stable)" />
  <img src="https://img.shields.io/badge/Python-3.11%2B-yellow" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Platform-Windows-blue" alt="Windows" />
  <img src="https://img.shields.io/badge/License-Proprietary-red" alt="Proprietary License" />
</p>

<p align="center">
  QuickBill is a Windows desktop billing and POS application designed for
  retail shops and small businesses. It provides a complete local billing
  workflow including product management, barcode scanning, inventory,
  payments, invoice generation, bill history, business configuration,
  and customer-facing display integration.
</p>

---

## Overview

QuickBill is designed to provide a fast, practical, and professional point-of-sale experience without requiring a cloud account or online business management platform.

The desktop application acts as the primary billing system and source of truth for products, inventory, bills, payments, and transaction data.

QuickBill can also integrate with companion applications such as the Customer Display and Barcode Scanner applications.

---

## What's New in v3.1.0

Version 3.1.0 focuses on application configuration, business identity, billing personalization, production stability, and overall usability.

### Business & Billing Configuration

- Added configurable UPI ID through application Settings.
- UPI ID is stored locally and persists between application restarts.
- Added configurable cashier name.
- Added configurable company/business name.
- Added configurable business owner name.
- Added business address configuration.
- Added business phone configuration.
- Added business email configuration.
- Added GST configuration.
- Configured business information is automatically used in generated invoices.
- Business information is reflected appropriately across 80 mm and A4 invoice formats.
- Default QuickBill information is used when optional business settings are left empty.

### Billing & Invoice Improvements

- Improved invoice personalization.
- Improved payment workflow.
- Improved UPI payment configuration.
- Improved invoice information layout.
- Improved 80 mm receipt formatting.
- Improved A4 invoice formatting.
- Improved billing workflow consistency.

### Application & Stability

- Improved application startup and initialization.
- Improved splash screen startup experience.
- Improved customer display initialization.
- Improved WebSocket-based customer display integration.
- Improved application configuration persistence.
- Improved production build configuration.
- Updated executable metadata to v3.1.0.
- Updated installer metadata to v3.1.0.
- Updated project licensing and copyright information.

---

## Features

### Point of Sale

- Fast billing workflow
- Barcode-based product lookup
- Manual barcode entry
- Add products directly to the current bill
- Increase and decrease item quantities
- Remove individual items
- Automatic subtotal calculation
- Automatic tax calculation
- Discount support
- Bill total calculation
- Bill number generation
- New bill workflow
- Hold and resume bills

### Product Management

- Add products
- Edit products
- Delete products
- Search products
- Barcode-based product identification
- Product pricing
- Product quantity management
- Inventory and stock management

### Barcode Scanning

- USB barcode scanner support
- Camera/IP barcode scanning support
- Continuous barcode scanning
- Automatic product lookup
- Duplicate barcode scanning with quantity updates
- Scanner status feedback

### Payments

- Cash payments
- UPI payments
- Card payments
- Credit payments
- Configurable UPI ID
- Dynamic UPI QR generation
- Payment confirmation workflow
- Payment transaction handling

### Invoice Generation

- Professional invoice generation
- 80 mm receipt format
- A4 invoice format
- Configurable business information
- Customer information
- Cashier information
- GST information
- Bill number
- Date and time
- Product details
- Quantity and pricing
- Tax and discount information
- Payment information

### Bill History

- View previous bills
- Search billing history
- Review completed transactions
- Reprint invoices
- Automatic bill numbering

### Customer Display

QuickBill can communicate with the companion Customer Display application to provide a real-time customer-facing billing experience.

The desktop application remains the authoritative billing system.

The Customer Display application receives billing and payment information from QuickBill and displays it to the customer.

### Application Settings

QuickBill provides configuration options for:

- UPI ID
- Cashier name
- Company/business name
- Owner name
- Business address
- Phone number
- Email address
- GST number
- Billing configuration

Settings are stored locally on the user's computer and persist between application sessions.

---

## QuickBill Ecosystem

QuickBill is part of a small ecosystem of applications designed to work together.

### QuickBill Desktop

The primary billing application and authoritative source for:

- Products
- Inventory
- Bills
- Payments
- Transactions
- Business configuration

Repository: https://github.com/kartikbansode/quickbill

Website: https://quickbill.kartikbansode.dev/

### Customer Display

A companion Android application providing a real-time customer-facing display for billing and payment information.

Repository: https://github.com/kartikbansode/quickbill-customer-display-app

### Barcode Scanner

A companion Android application that can be used as a barcode scanner for QuickBill Desktop.

Repository: https://github.com/kartikbansode/quickbill-barcode-scanner-app

---

## Screenshots

### Billing Window

<img
  width="1919"
  height="1079"
  alt="QuickBill Billing Window"
  src="https://github.com/user-attachments/assets/a7da29cc-d3e1-47d2-a949-7c3a4842206b"
/>

### Product Management

<img
  width="1919"
  height="1079"
  alt="QuickBill Product Management"
  src="https://github.com/user-attachments/assets/12a94658-4a30-4b03-986a-eeb3cc6795fb"
/>

### Invoice — 80 mm

<img
  width="347"
  height="826"
  alt="QuickBill 80mm Invoice"
  src="https://github.com/user-attachments/assets/5b73904e-bc3e-4373-9fc0-c13501e12a9d"
/>

### Invoice — A4

<img
  width="671"
  height="842"
  alt="QuickBill A4 Invoice"
  src="https://github.com/user-attachments/assets/b87f7430-563c-400b-b93d-4c637720cee1"
/>

---

## Requirements

- Windows 10 or Windows 11
- Python 3.11 or newer
- Webcam or compatible barcode scanner for barcode scanning features

---

## Installation

### Option 1 — Windows Installer

Download the latest QuickBill installer from the GitHub Releases page:

https://github.com/kartikbansode/quickbill/releases

Run the installer and follow the installation wizard.

After installation, launch QuickBill from the Start Menu or desktop shortcut.

### Option 2 — Run From Source

Clone the repository:

```bash
git clone https://github.com/kartikbansode/quickbill.git
```

Enter the project directory:

```bash
cd quickbill
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run QuickBill:

```bash
python app.py
```

---

## Initial Configuration

After launching QuickBill for the first time, open the application Settings.

Configure the following information if required:

- UPI ID
- Cashier name
- Company/business name
- Owner name
- Address
- Phone
- Email
- GST number

These settings are stored locally on the computer and are automatically used by QuickBill during future sessions.

If a business field is left empty, QuickBill uses its default application information where applicable.

---

## UPI Configuration

UPI payments can be configured directly from the QuickBill Settings section.

Enter the UPI ID that should be used for payment QR generation.

Example:

```text
yourname@upi
```

The configured UPI ID is stored locally on the user's computer.

There is no need to modify the source code after installation.

---

## Building the Executable

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Build QuickBill using the production PyInstaller specification:

```bash
pyinstaller --clean QuickBill.spec
```

The executable will be generated inside:

```text
dist/
```

The resulting application is:

```text
dist/QuickBill.exe
```

---

## Building the Windows Installer

The QuickBill installer is created using Inno Setup.

The installer configuration is located at:

```text
installer/QuickBill.iss
```

The production installer output is:

```text
release/QuickBill_Setup_v3.1.0.exe
```

---

## Project Structure

```text
quickbill/
│
├── app.py
├── requirements.txt
├── QuickBill.spec
│
├── assets/
│   └── images/
│
├── gui/
│   ├── billing/
│   ├── settings/
│   └── ...
│
├── logic/
│   ├── database/
│   ├── customer_display_server/
│   └── ...
│
├── installer/
│   ├── QuickBill.iss
│   ├── wizard.bmp
│   └── wizard_small.bmp
│
├── version/
│   └── version_info.txt
│
├── licenses/
│   └── LICENSE.txt
│
└── README.md
```

---

## Data & Privacy

QuickBill is primarily a local desktop application.

Application data and configuration are stored locally on the user's computer unless an explicitly configured external integration is used.

QuickBill does not require a mandatory online account for its core billing functionality.

Users are responsible for maintaining appropriate backups of their business and billing data.

---

## Third-Party Components

QuickBill uses third-party libraries and technologies to provide functionality such as:

- Python
- Tkinter
- OpenCV
- PyZBar
- ReportLab
- QRCode
- Pygame
- PyInstaller
- WebSockets
- Pillow
- Python Barcode
- VLC

Each third-party component remains subject to its respective license.

QuickBill does not claim ownership of third-party software, libraries, frameworks, or components.

---

## Version

Current release:

```text
QuickBill 3.1.0
```

Release type:

```text
Stable Release
```

---

## License

QuickBill is proprietary software.

Copyright © 2026 Kartik Bansode. All Rights Reserved.

The source code is publicly available for viewing, educational, portfolio, evaluation, academic, and professional purposes subject to the terms of the proprietary license.

No permission is granted to copy, reproduce, modify, redistribute, commercially use, sublicense, sell, or create derivative works from this software or its source code without prior written permission from the copyright holder.

See the complete license:

[https://github.com/kartikbansode/quickbill/blob/main/LICENSE](https://github.com/kartikbansode/quickbill/blob/main/LICENSE)

---

## Official Links

**QuickBill Website**

[https://quickbill.kartikbansode.dev/](https://quickbill.kartikbansode.dev/)

**GitHub Repository**

[https://github.com/kartikbansode/quickbill](https://github.com/kartikbansode/quickbill)

**Releases**

[https://github.com/kartikbansode/quickbill/releases](https://github.com/kartikbansode/quickbill/releases)

**Customer Display**

[https://github.com/kartikbansode/quickbill-customer-display-app](https://github.com/kartikbansode/quickbill-customer-display-app)

**Barcode Scanner**

[https://github.com/kartikbansode/quickbill-barcode-scanner-app](https://github.com/kartikbansode/quickbill-barcode-scanner-app)

---

## Developer

**Kartik Bansode**

GitHub: [https://github.com/kartikbansode](https://github.com/kartikbansode)

QuickBill: [https://quickbill.kartikbansode.dev/](https://quickbill.kartikbansode.dev/)

---

<p align="center">
  <strong>QuickBill 3.1.0</strong>
  <br>
  Professional Desktop Billing & POS Management System
  <br><br>
  © 2026 Kartik Bansode. All Rights Reserved.
</p>