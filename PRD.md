# Product Requirements Document (PRD)

**Product:** QuickBill  
**Version:** 3.1.0  
**Release:** Stable Release  
**Status:** Implemented

---

# 1. Product Overview

QuickBill is a native Windows desktop Point-of-Sale (POS) and billing application built with Python and Tkinter.

It provides retail businesses with a professional local-first billing system for processing transactions, managing products, handling barcode-based billing, generating invoices, managing billing history, configuring business information, processing payments, and communicating with a customer-facing display.

QuickBill is designed to provide a reliable and efficient checkout experience without requiring a mandatory cloud account or subscription.

The desktop application remains the authoritative source for billing, products, inventory, payments, and transaction state.

---

# 2. Product Vision

To provide small and medium-sized retail businesses with a professional, reliable, fast, and easy-to-use desktop POS system that delivers the essential functionality of modern commercial billing software while remaining lightweight, locally operated, and extensible.

---

# 3. Target Users

QuickBill is designed primarily for:

- Retail shop owners
- Cashiers
- Store managers
- General retail stores
- Grocery and supermarket businesses
- Hardware stores
- Small business operators
- Other businesses requiring local desktop billing

---

# 4. Problem Statement

Many small businesses continue to use outdated billing systems that provide poor user interfaces, limited customization, slow workflows, or unnecessary complexity.

Modern POS solutions can also introduce recurring subscription costs, cloud dependencies, and infrastructure requirements.

QuickBill aims to provide a professional desktop alternative with:

- Fast checkout
- Local data storage
- Barcode-based billing
- Product management
- Payment support
- Professional invoice generation
- Business configuration
- Customer display integration
- Simple installation and operation

---

# 5. Core Features

## 5.1 Billing Workflow

QuickBill provides a streamlined billing workflow designed for fast cashier operation.

### Cart Management

- Add products to the current bill.
- Add products using barcode scanning.
- Add products manually.
- Increase item quantity.
- Decrease item quantity.
- Remove individual items.
- Display item actions directly within the cart.
- Automatically update totals after cart changes.
- Prevent invalid billing states.

### Billing Calculation

The application dynamically calculates:

- Item subtotal
- Quantity-based totals
- Tax
- Discounts
- Grand total

### Bill Generation

The bill generation workflow supports:

- Customer name
- Customer phone number
- Cashier information
- Business information
- Invoice number
- Date and time
- Product details
- Quantity
- Pricing
- Tax
- Discount
- Payment information

Generated transactions are saved to local billing history.

---

## 5.2 Barcode Scanner

QuickBill supports barcode-based product identification.

### Scanner Capabilities

- USB barcode scanner support
- Camera-based barcode scanning
- IP camera scanning
- OpenCV-based camera processing
- PyZBar barcode detection
- Continuous scanning
- Successful-scan audio feedback
- Duplicate scan protection
- Automatic product lookup
- Automatic cart quantity update

The scanner should remain responsive during normal billing operations.

---

## 5.3 Product Management

QuickBill provides a dedicated product management interface.

### Product Operations

- Add products
- Edit products
- Delete products
- Search products
- Find products by barcode
- Find products by name
- Configure product prices
- Manage product information

Product data is maintained locally.

---

## 5.4 Billing History

QuickBill maintains a local history of completed bills.

### History Capabilities

- Store completed transactions
- Search previous bills
- Search by invoice number
- Search by customer name
- Search by customer phone
- View previous transaction information
- Reprint invoices
- Review transaction details

Billing history persists between application sessions.

---

## 5.5 Invoice Generation

QuickBill supports professional invoice generation using ReportLab.

### Supported Formats

- 80 mm receipt
- A4 invoice

### Invoice Information

Invoices can contain:

- Company/business name
- Owner name
- Business address
- Phone number
- Email address
- GST number
- Cashier name
- Invoice number
- Date
- Time
- Customer information
- Product name
- Quantity
- Unit price
- Item total
- Tax
- Discount
- Grand total
- Payment method
- UPI information where applicable

Business information is configurable through the application Settings.

If optional business information is not configured, QuickBill uses its default application information where applicable.

Generated invoices can be opened using the system's default PDF viewer.

---

## 5.6 Payment System

QuickBill provides an integrated payment workflow.

### Supported Payment Methods

- Cash
- UPI
- Card
- Credit

### Cash Payment

The payment workflow can calculate:

- Amount payable
- Cash received
- Change to return

### UPI Payment

QuickBill supports:

- Configurable UPI ID
- Dynamic UPI QR generation
- Payment amount encoded into the QR
- UPI payment display during checkout

The UPI ID is configured directly from the application Settings.

The configured UPI ID is stored locally and remains available after restarting the application.

---

## 5.7 Customer Display

QuickBill can communicate with the companion Customer Display application.

The desktop application is the authoritative source of billing state.

The Customer Display receives and displays relevant information such as:

- Current cart
- Product information
- Quantities
- Subtotal
- Tax
- Discount
- Grand total
- Payment information
- Payment success state

The customer-facing application must not independently calculate or modify the authoritative bill.

---

## 5.8 Business Configuration

QuickBill provides configurable business information through Settings.

### Configurable Information

- UPI ID
- Cashier name
- Company/business name
- Owner name
- Address
- Phone number
- Email address
- GST number

Configuration is stored locally on the user's computer.

The settings remain available after:

- Closing the application
- Restarting the application
- Restarting the computer

Configured information is automatically used where appropriate throughout billing and invoice generation.

---

## 5.9 Application Settings

The Settings section provides centralized configuration for application and business-related information.

Settings should be presented using a consistent UI design and should provide clear labels, appropriate input controls, validation, and persistent storage.

---

# 6. UI/UX Requirements

QuickBill should maintain a consistent professional desktop application interface.

## Visual Design

The application should use:

- Consistent typography
- Consistent button styling
- Consistent spacing
- Consistent borders and panels
- Consistent input fields
- Consistent dialogs
- Clear visual hierarchy
- Professional POS-oriented layouts

The UI should avoid unnecessary decorative elements that interfere with the billing workflow.

## Responsiveness

The application should adapt to different Windows desktop and laptop resolutions.

Layouts should use appropriate Tkinter `grid` and `pack` configuration so that:

- Tables remain usable
- Buttons remain accessible
- Text does not become unnecessarily clipped
- Panels resize appropriately
- Billing controls remain visible
- Smaller laptop screens remain usable
- Larger displays utilize available space effectively

## Billing Status

The billing status information should remain limited to the appropriate billing interface and should not unnecessarily appear throughout unrelated application screens.

## Splash Screen

QuickBill uses a dedicated startup splash screen while the application initializes required components.

The splash screen should:

- Display QuickBill branding
- Remain visually stable
- Avoid unnecessary animation
- Avoid blurry graphics
- Display readable text
- Provide meaningful initialization status
- Close automatically after successful initialization

---

# 7. Application Startup

The startup process should initialize the required application components before displaying the main application.

Startup components may include:

- Application configuration
- Product data
- Billing history
- Required application services
- Customer Display communication service
- Other required runtime components

Startup failures should be handled gracefully without leaving the application in an unusable state.

---

# 8. Error Handling

QuickBill should prioritize graceful error handling.

The application should:

- Handle missing hardware gracefully.
- Handle unavailable cameras without crashing.
- Handle unavailable customer displays gracefully.
- Handle invalid configuration values.
- Handle missing optional configuration.
- Prevent raw exceptions from being unnecessarily exposed to normal users.
- Provide useful error messages when user intervention is required.
- Continue operating when optional integrations are unavailable.

---

# 9. Data Storage

QuickBill is designed as a local-first desktop application.

Current application data uses local files including:

```text
products.json
bills_history.json
config.json
```

### Configuration

Application configuration is stored locally and persists between sessions.

### Billing Data

Completed billing transactions are stored locally.

### Product Data

Product information is stored locally and loaded by the application during operation.

---

# 10. Data Integrity

The application should ensure that:

- Billing totals are calculated consistently.
- Completed transactions are saved reliably.
- Configuration changes persist correctly.
- Product changes persist correctly.
- Customer Display data reflects the authoritative desktop application state.
- Invalid transactions are prevented wherever possible.

The desktop application remains the source of truth for billing and transaction information.

---

# 11. Security & Privacy

QuickBill is primarily a local desktop application.

Core application data is stored locally on the user's computer.

Users are responsible for:

- Protecting their computer.
- Maintaining appropriate backups.
- Verifying business information.
- Verifying tax information.
- Verifying payment information.
- Protecting locally stored business data.

Third-party integrations remain subject to the policies and terms of their respective providers.

---

# 12. Production Requirements

The production release should provide:

- Windows executable
- Windows installer
- Application icon
- Version metadata
- Installer version metadata
- Proper uninstaller
- Start Menu shortcut
- Optional desktop shortcut
- Production PyInstaller configuration
- Production Inno Setup configuration
- Application license
- Version information
- Updated documentation

Current stable version:

```text
QuickBill 3.1.0
```

---

# 13. Supported Environment

## Operating System

- Windows 10
- Windows 11

## Development Runtime

- Python 3.11+

## Major Technologies

- Python
- Tkinter
- OpenCV
- PyZBar
- ReportLab
- Pillow
- QRCode
- Pygame
- WebSockets
- PyInstaller
- Inno Setup

---

# 14. Project Architecture

QuickBill follows a modular application structure.

Major application areas include:

```text
Application Entry Point
        |
        ├── Startup / Splash
        |
        ├── Main Window
        |
        ├── Billing
        │     ├── Cart
        │     ├── Scanner
        │     ├── Totals
        │     └── Payment
        |
        ├── Product Management
        |
        ├── Billing History
        |
        ├── Settings
        |
        ├── Invoice Generation
        |
        ├── Local Data Storage
        |
        └── Customer Display Server
```

The architecture should remain modular so individual components can be improved without unnecessarily affecting unrelated application modules.

---

# 15. Release Information

**Current Version:** 3.1.0

**Release Status:** Stable Release

**Product:** QuickBill

**Copyright:** © 2026 Kartik Bansode

**Official Website:**

[https://quickbill.kartikbansode.dev/](https://quickbill.kartikbansode.dev/)

**Official Repository:**

[https://github.com/kartikbansode/quickbill](https://github.com/kartikbansode/quickbill)

---

# 16. Future Roadmap

The following features may be considered for future releases:

- Migration from JSON storage to SQLite.
- Improved relational data integrity.
- Advanced inventory management.
- Stock-in and stock-out management.
- Low-stock alerts.
- Advanced reporting.
- Sales analytics.
- Expense management.
- ESC/POS thermal printer integration.
- Improved printer configuration.
- Role-based access control.
- Admin and cashier permissions.
- Multi-terminal architecture.
- Optional cloud synchronization.
- Automated backups.
- Advanced customer management.
- Supplier management.
- Improved reporting and business analytics.

These features are planned for future development and are not considered requirements of the current stable release unless explicitly implemented.

---

# 17. Licensing

QuickBill is proprietary software.

Copyright © 2026 Kartik Bansode. All Rights Reserved.

The source code is publicly available for viewing, educational, portfolio, evaluation, academic, and professional purposes subject to the terms of the project's proprietary license.

No rights are granted to copy, reproduce, modify, redistribute, commercially use, sublicense, sell, or create derivative works from the software or its source code without prior written permission from the copyright holder.

See:

[https://github.com/kartikbansode/quickbill/blob/main/LICENSE](https://github.com/kartikbansode/quickbill/blob/main/LICENSE)

---

# 18. Official Resources

**QuickBill Website**

[https://quickbill.kartikbansode.dev/](https://quickbill.kartikbansode.dev/)

**GitHub Repository**

[https://github.com/kartikbansode/quickbill](https://github.com/kartikbansode/quickbill)

**GitHub Releases**

[https://github.com/kartikbansode/quickbill/releases](https://github.com/kartikbansode/quickbill/releases)

**Customer Display Application**

[https://github.com/kartikbansode/quickbill-customer-display-app](https://github.com/kartikbansode/quickbill-customer-display-app)

**Barcode Scanner Application**

[https://github.com/kartikbansode/quickbill-barcode-scanner-app](https://github.com/kartikbansode/quickbill-barcode-scanner-app)

---

# 19. Developer

**Kartik Bansode**

GitHub: [https://github.com/kartikbansode](https://github.com/kartikbansode)

QuickBill: [https://quickbill.kartikbansode.dev/](https://quickbill.kartikbansode.dev/)

---

# 20. Release Statement

QuickBill 3.1.0 represents the Stable Release of the current production application.

The release establishes the foundation for future improvements in billing, inventory, payments, reporting, hardware integration, and business management functionality.