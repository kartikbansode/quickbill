# QuickBill v3.1.0
**Project Identity:** Professional Desktop Point of Sale (POS) & Billing Application
**Version:** 3.1.0 (First Stable Release)
**Status:** Stable Production Ready

## 1. Project Purpose
QuickBill Pro is a high-end, responsive, and robust Windows desktop billing application designed for real retail environments (supermarkets, medical shops, hardware stores). It aims to replace messy, outdated POS software with a modern, beautifully designed Tkinter interface that offers seamless keyboard navigation, fast barcode scanning, automated PDF receipt generation, and a separate Customer Display Server.

## 2. Core Architecture
- **Language**: Python 3.11+
- **GUI Framework**: Tkinter (Native desktop rendering)
- **Design Pattern**: Modular components (`gui/`, `logic/`), Custom styling layer leveraging `gui.ui_components`.
- **Database**: In-memory JSON stub simulation (`products.json`, `bills_history.json`).
- **Threading**: Main thread handles Tkinter UI. Background threads handle Barcode Scanner and Customer Display WebSocket server.

## 3. Technology Stack
- **UI**: Tkinter, ttk (Clam theme)
- **Barcode Parsing**: OpenCV, Pyzbar (`logic/barcode_scanner.py`)
- **PDF Generation**: ReportLab (`logic/pdf_generator.py`)
- **Image Processing**: Pillow (PIL)
- **Audio Feedback**: Pygame (for scanner beeps)
- **Networking/Display**: Asyncio + WebSockets (`logic/customer_display_server.py`)

## 4. Modules & Responsibilities
### Application Entry
- `app.py`: Bootstrapper. Handles the hidden root creation, triggers the `SplashScreen`, coordinates synchronous initialization steps, and hands off to `launch_main_window()`.

### GUI (`gui/`)
- `splash_screen.py`: Professional fading splash screen with a synchronous progress bar.
- `main_window.py`: The master window container. Initializes `FindBillView`, `Toolbar`, and handles application exit logic.
- `billing/`:
  - `billing_view.py`: Master billing view controller. Contains left/right layout.
  - `cart_table.py`: Renders the current bill table.
  - `totals_panel.py`: Calculates Subtotal, Tax, Discount, Grand Total.
  - `scanner_panel.py`: Shows live webcam feed if active.
- `dialogs/`: Various popup modules (Add product, Payment, etc.).
- `ui_components.py`: Centralized UI library enforcing QuickBill's design system (colors, buttons, typography).

### Logic (`logic/`)
- `database.py`: Product and Bill persistence layer.
- `customer_display_server.py`: Runs a WebSocket server (TCP 8765) and a UDP discovery server (UDP 8766) to broadcast live cart updates to an Android client.
- `pdf_generator.py`: Converts completed bills into A4 PDF receipts.

## 5. Important Design Decisions
- **Synchronous Splash**: `splash_screen.py` uses blocking event loops (`time.sleep(0.015) + update_idletasks()`) to ensure loading messages stay on screen and the window transition has no visual tearing.
- **Deiconify Late**: `window.deiconify()` is called at the absolute end of `launch_main_window()` to prevent rendering an unconfigured 200x200 blank window.
- **Authoritative Desktop**: The desktop application is the single source of truth. The Customer Display only receives read-only state updates.
- **No Dummy Buttons**: All buttons in the UI are functional. Placeholders for "Reports" and "Customers" were explicitly removed for the stable release.
- **Strict Theme**: `gui/ui_components.py` dictates the design language (colors: `#102A43` background, `#2F6FED` primary accent).

## 6. Execution Instructions
Run from the root directory:
```bash
python -u app.py
```
