# Product Requirements Document (PRD)
**Product:** QuickBill Pro
**Version:** 3.0.0 (First Stable Release)
**Status:** IMPLEMENTED

## 1. Product Overview
QuickBill Pro is a native Windows desktop point-of-sale (POS) and billing application built on Python and Tkinter. It provides retail shops with a highly professional, reliable, and keyboard-driven interface to process transactions, manage carts, generate PDF receipts, and broadcast live checkout data to a customer-facing display.

## 2. Product Vision
To completely modernize the checkout experience for small-to-medium retail businesses by providing a beautifully designed, premium POS system that rivals expensive commercial software but remains lightweight and extensible.

## 3. Target Users
- Cashiers in supermarkets, medical shops, hardware stores, and general retail.
- Store managers who need reliable PDF receipts and a simple product database.

## 4. Problem Statement
Many small retail stores rely on legacy DOS-based or outdated web-wrapped POS systems that are ugly, unresponsive, and difficult to navigate. Modern alternatives are often expensive cloud-based subscriptions. Retailers need a fast, native, local-first billing application that feels premium.

---

## 5. Core Features (Implemented in v3.0.0)

### 5.1 Billing Workflow
- **Master Interface:** Left panel for product searching/scanning, Right panel for the active cart.
- **Cart Management:** Add products, dynamically increment/decrement quantities using inline UI buttons, remove items.
- **Dynamic Calculation:** Instantly calculates subtotals, tax, discounts, and the grand total on every cart modification.
- **Bill Generation:** "Generate Bill" captures customer details (Name, Phone), creates a PDF, and saves the transaction to history.
- **Keyboard Shortcuts:** `F2` (New Bill) and `F4` (Generate/Pay) for rapid cashier operations.

### 5.2 Barcode Scanner
- **Live Feed:** Utilizes OpenCV and Pyzbar to read camera feeds (USB or IP webcam).
- **Audio Feedback:** Pygame integration provides an audible "beep" on successful scan.
- **Duplicate Delay:** Prevents accidental double-scanning of the same item within a specified cooldown period (e.g., 1 second).

### 5.3 Product Management
- **In-Memory Store:** Loads products from `products.json`.
- **UI Browsing:** "Products" view displays all available items in a structured Tkinter Treeview.
- **Searchable:** Instant search filtering by product name or ID.

### 5.4 Billing History
- **Persistence:** Stores generated bills in `bills_history.json`.
- **Find Bill:** Dedicated interface to search past bills by Invoice Number, Customer Name, or Phone.
- **Reprinting:** Ability to view details of a past bill and reprint the PDF.

### 5.5 PDF Generation
- **ReportLab Engine:** Generates A4-sized PDF receipts.
- **Formatting:** Includes store header, invoice metadata, line items (Qty, Price, Total), and grand totals.
- **Automation:** Auto-opens the PDF in the system's default viewer upon generation.

### 5.6 Customer Display Server
- **Architecture:** Runs an Asyncio WebSocket Server (`TCP 8765`) and UDP Broadcast Server (`UDP 8766`).
- **One-Way Sync:** The Desktop App is the authoritative source. It broadcasts cart items, totals, and payment success to any connected Android tablet.

### 5.7 Payment / UPI Functionality
- **Modal Dialog:** Clean, dark-themed payment window.
- **Calculation:** Auto-calculates exact change based on cashier's inputted cash received.
- **UPI QR:** Generates and displays a dynamic UPI QR code on the screen for cashless checkout.

---

## 6. UI/UX Requirements
- **Theme:** Strict adherence to a professional Dark Navy theme (`#102A43` background, `#2F6FED` accent, `#FFFFFF` text).
- **Responsiveness:** The layout uses Tkinter `grid` and `pack` weights to gracefully scale to smaller laptops and ultra-wide monitors without clipping widgets.
- **Startup:** A premium, synchronous splash screen masking all database, network, and UI initialization. 

## 7. Error Handling
- **Graceful Failures:** Missing webcams fall back smoothly without crashing the app.
- **Exception Masking:** Startup errors are caught and logged, preventing raw tracebacks from freezing the GUI.
- **No Dummy Controls:** All non-implemented features have been explicitly stripped from the GUI to prevent user confusion.

## 8. Data / Database Requirements
- **Storage:** Flat-file JSON (`products.json`, `bills_history.json`, `config.json`).
- **Integrity:** Local data read on startup; writes persist immediately upon checkout.

---

## 9. Future Roadmap (Planned)
- Migration to SQLite or PostgreSQL for relational data integrity.
- Cloud syncing and multi-terminal architectures.
- Role-based Access Control (Admin vs. Cashier).
- ESC/POS thermal printer integration (removing reliance on A4 PDFs).
- Inventory tracking (Stock in/out management).
