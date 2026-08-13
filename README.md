<div align="center">
  <img src="assets/images/logo.png" alt="QuickBill Pro Logo" width="120" />
  <h1>QuickBill Pro v3.0.0</h1>
  <p><strong>Professional Point of Sale (POS) & Billing Desktop Application</strong></p>

  [![Version](https://img.shields.io/badge/Version-3.0.0-blue)](https://github.com/kartikbansode/quickbill)
  [![Platform](https://img.shields.io/badge/Platform-Windows-green)](#)
  [![Python](https://img.shields.io/badge/Python-3.11+-blue)](#)
</div>

## Overview
QuickBill Pro is a comprehensive, high-end retail billing and Point of Sale (POS) application designed specifically for modern supermarkets, hardware stores, medical shops, and general retail. Featuring a beautiful and highly responsive dark-themed Tkinter interface, QuickBill Pro empowers cashiers with seamless keyboard navigation, instant barcode scanning, one-click PDF generation, and real-time synchronization with a wireless Customer Display.

---

## 🚀 Core Features
*   **Lightning Fast Billing:** Keyboard-first workflow designed for high-throughput retail environments (`F2` for New Bill, `F4` for Checkout).
*   **Integrated Barcode Scanner:** Real-time webcam barcode parsing using OpenCV & Pyzbar with audible beep feedback.
*   **Dual View Customer Display:** Automatically broadcasts the live cart and checkout totals to any Android device on the network via WebSockets.
*   **Automated PDF Receipts:** Instantly generates professional A4 PDF invoices upon checkout using ReportLab.
*   **UPI / Payment Integration:** Built-in modal for unified payment processing and exact change calculation.
*   **Intelligent Cart Management:** In-line editing (`+`, `-`, `Trash`) with instantaneous subtotal, tax, and discount recalcs.

---

## 🛠 Technology Stack
*   **Language:** Python 3.11+
*   **GUI Framework:** Native `Tkinter` (Custom TTK Clam Theme)
*   **Vision & Scanning:** `OpenCV` (`cv2`), `pyzbar`
*   **Document Generation:** `reportlab`
*   **Networking:** `asyncio`, `websockets` (Customer Display Server)
*   **Database:** High-speed in-memory JSON (`products.json`, `bills_history.json`)

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kartikbansode/quickbill.git
   cd quickbill
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch QuickBill Pro:**
   ```bash
   python -u app.py
   ```

---

## ⚙️ Configuration
The configuration is stored in `config.json`. You can modify it manually or through the application's Settings menu.
```json
{
    "scanner": {
        "type": "mobile_camera",
        "camera_url": "", 
        "duplicate_delay": 1,
        "beep": true
    }
}
```
*Note: If you use a mobile IP webcam, set the `camera_url` (e.g. `http://192.168.1.50:8080/video`). If left blank, it will attempt to use your default connected USB webcam.*

---

## 📱 Customer Display Setup
QuickBill Pro hosts a local WebSocket server on `TCP 8765` and broadcasts its presence via `UDP 8766`.
1. Ensure the desktop running QuickBill and the Android tablet/phone are on the **same Wi-Fi network**.
2. Launch the QuickBill application. The server starts automatically in the background.
3. Open the companion Customer Display App on your tablet; it will auto-discover the desktop and sync instantly.

---

## 📝 Limitations & Roadmap
**v3.0.0 Scope Limitations:**
*   **Database:** Currently utilizes JSON stubs. Planned migration to SQLite/PostgreSQL for multi-terminal sync.
*   **Authentication:** Single user mode only. No cashier login or role-based access control yet.
*   **Inventory:** Tracks products but does not track dynamic stock counts/deductions.

**Future Roadmap (v4.0.0+):**
*   [ ] Cloud-sync & Multi-terminal support.
*   [ ] Inventory tracking with low-stock alerts.
*   [ ] Detailed analytics and daily shift reports.
*   [ ] Hardware ESC/POS Thermal Printer support.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
