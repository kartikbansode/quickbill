# QuickBill - Complete Project Context v2.1.0

## 1. Project Information
**Project Name:** QuickBill | **Version:** v2.1.0 | **Type:** Desktop Billing & Inventory Management Software | **Language:** Python 3.11 | **OS:** Windows | **UI Framework:** Tkinter | **License:** MIT | **Packaging:** PyInstaller | **Installer:** Inno Setup | **Repository:** https://github.com/kartikbansode/quickbill

## 2. Project Goal
QuickBill is a complete desktop billing software for small businesses, retail shops, grocery stores and local stores. Objective: Provide lightweight but professional billing system without internet connection or external database. Application stores all data locally. Everything designed to be simple, fast and professional.

## 3. Design Philosophy
**Principles:** Lightweight, Offline First, Fast Startup, Professional UI, Easy Maintenance, Modular Architecture, No unnecessary dependencies, Easy future expansion. Every module performs one responsibility. Business logic never mixed with UI.

## 4. Current Version
**Version:** 2.0.0 | **Status:** Stable | **Major Milestone:** Professional Windows Desktop Application

**Completed Features:** ✓ Billing System, ✓ Product Management, ✓ Barcode Scanner, ✓ Barcode Label Generator, ✓ PDF Invoice Generator, ✓ Hold Bills, ✓ Bill History, ✓ Search Bills, ✓ Settings, ✓ Installer, ✓ Uninstaller, ✓ Version Information, ✓ Runtime Data Storage, ✓ Professional Packaging

## 5. Technology Stack
**Programming:** Python 3.11 | **GUI:** Tkinter | **PDF Generation:** ReportLab | **Barcode Generation:** ReportLab Code128 | **Barcode Reading:** pyzbar | **Camera:** OpenCV | **Sound:** pygame | **Packaging:** PyInstaller | **Installer:** Inno Setup | **Version Resource:** Windows VERSIONINFO | **Icons:** ICO | **Fonts:** DejaVu Font Family | **Storage:** JSON Files

## 6. Project Structure
**Root:** QuickBill/ | **Folders:** assets/, gui/, logic/, installer/, licenses/, version/ | **Files:** app.py, QuickBill.spec, requirements.txt, README.md, LICENSE, .gitignore, PROJECT_CONTEXT.md

## 7. assets/ Folder
**Purpose:** Stores static resources. **Subfolders:** fonts/ (DejaVu fonts for PDF generation), images/ (logo.png, logo.ico for app icon/installer/taskbar), sounds/ (beep.mp3 for barcode scanner success)

## 8. gui/ Folder
**Purpose:** Contains UI components. GUI never directly manipulates files, always calls logic/. Responsible for: Displaying data, Receiving user input, Calling business logic, Updating interface. **Subfolders:** billing/, dialogs/, payment/, find_bill/, hold_bill/. **Main Files:** main_window.py (controller), header.py (branding), toolbar.py (navigation), statusbar.py (status info), product_master.py (product management), settings_view.py (settings), splash_screen.py (loading screen)

## 9. logic/ Folder
**Purpose:** Contains business logic. Never contains UI code, all reusable without Tkinter. **Modules:** database.py (CRUD, JSON storage), config.py (settings), cart.py (cart logic), billing.py (price calculations), barcode_scanner.py (camera scanning), barcode_pdf.py (barcode sheet generation), pdf_generator.py (invoice generation), bill_history.py (bill search), hold_bill.py (hold functionality), resource_path.py (access bundled assets), app_dirs.py (runtime directory)

## 10. Runtime Data
QuickBill separates: **Application files** (Executable, Assets, Fonts, Images, Installer - never change) from **User files** (Products, Bills, History, Config, Barcode PDFs, Generated invoices - writable)

## 11. Runtime Storage
All writable files stored in LocalAppData (not Program Files which is read-only). Benefits: Cleaner installation, Safer updates, Professional behavior (same as commercial Windows apps)

## 12. Resource System
**resource_path():** Load bundled assets (Fonts, Images, Icons, Sounds, Logo) - read-only, packaged into executable. **data_path():** Load writable data (products.json, config.json, bill_counter.json, held_bills.json, bills_history.json, Generated PDFs) - auto-created on first launch

## 13. JSON Database
**Reason chosen:** Simple, Portable, Human readable, Easy backup/restore/debugging. **Current files:** products.json (all products), config.json (application settings), bill_counter.json (invoice counter), held_bills.json (held bills), bills_history.json (completed bills)

## 14. Build System
**Development:** python app.py | **Production:** PyInstaller with spec file (QuickBill.spec) produces dist/ containing QuickBill.exe (one-file executable, professional Windows application)

## 15. Installer
**Technology:** Inno Setup | **Capabilities:** Professional wizard, Desktop shortcut, Start Menu shortcut, Uninstaller, Version information, License, Company information, Application icon, Modern wizard style, Compression enabled, Professional installation experience

## 16. Coding Standards
**Naming:** snake_case for variables, PascalCase for classes, UPPER_CASE for constants | **Indentation:** 4 spaces | **Encoding:** UTF-8 | **Paths:** Always use helper functions, never hardcoded file paths

---

# PART 2: APPLICATION ARCHITECTURE

## 17. Overall Software Architecture
**Three major layers:** Presentation Layer (gui/) - Displays windows, Takes input, Renders tables, Shows dialogs, Updates UI. Never performs file writing, database operations, calculations, business decisions | Business Logic Layer (logic/) - Calculations, Barcode processing, Database operations, Invoice generation, Cart management, Configuration. Independent of Tkinter | Data Layer (JSON) - Stores Products, Bills, Settings, History, Counters, Held Bills. Easy backup, migration, editing, no installation required, portable

## 18. Startup Flow
**Execution order:** app.py → Splash Screen → Initialize Product Database → Initialize Bill Database → Prepare Runtime Environment → Load Configuration → Initialize Scanner → Launch Main Window → Application Ready

## 19. app.py
**Purpose:** Entry point. **Responsibilities:** Display splash screen, Initialize databases, Load runtime, Start main window. Never place business logic here.

## 20. Splash Screen
**Purpose:** Professional startup experience. **Progress Sequence:** 10% Initializing QuickBill, 30% Loading Product Database, 55% Loading Billing History, 75% Preparing Workspace, 90% Initializing Barcode Scanner, 100% Launching Application. Once complete: Splash closes, Main window opens

## 21. Main Window
**File:** main_window.py | **Role:** Application controller. **Components created:** Header, Toolbar, Billing View, Product Master, Settings, Bill History, Status Bar, Payment Dialog, Hold Bill Window, Barcode Scanner. Controls navigation, should not contain database code

## 22. Navigation System
**Method:** Toolbar buttons → Corresponding View → Hide Previous View → Show Requested View. Only one major page visible. **Views:** Billing, Products, Settings, Find Bills, (Future: Reports, Customers, Analytics)

## 23. Billing Workflow
Customer arrives → Cashier scans barcode → Scanner returns barcode → Database searches product → Product found → Add to cart → Refresh totals → Generate bill → Payment dialog → Generate PDF → Reduce stock → Save history → Clear cart → Generate next invoice

## 24. Product Workflow
**Add:** Validate Data → Save JSON → Refresh Table | **Edit:** Open Product Master → Search → Edit → Save → Update JSON → Refresh Table | **Delete:** Confirmation → Remove JSON → Refresh Table

## 25. Barcode Scanner Workflow
Camera → OpenCV → Frame → Convert Gray → Crop ROI → pyzbar Decode → Barcode Found → Cooldown Check → Callback → Database Search → Add Product → Play Sound → Refresh Cart. Prevents: Duplicate scans, False reads, Continuous spam

## 26. Barcode Generator Workflow
User → Product Master → Print Barcode → Barcode Dialog → Select Products → Generate Labels → ReportLab → barcode_labels.pdf → Open Automatically

## 27. Invoice Workflow
Cart Ready → Payment → Generate Invoice Number → Calculate Totals → Create PDF → Save JSON → Reduce Stock → History Updated → Cart Cleared

## 28. Runtime Data Flow
Scanner → Database → Cart → Billing Engine → PDF Generator → History → User. Every module performs one task, no duplicated responsibilities

## 29. Module Communication
GUI → logic.database → logic.cart → logic.billing → logic.pdf_generator → JSON Files. GUI never directly edits JSON, only logic modules perform file operations

## 30. Resource Loading
**Bundled Assets:** resource_path() | **Runtime Data:** data_path(). Never mix both. Assets read-only, Runtime data writable

## 31. Configuration System
**config.json stores:** Company Name, Owner, GST, Phone, Email, Logo, Currency, Tax, Discount, Scanner URL, Scanner Type, Scanner Delay, Scanner Beep. Future settings also stored here

## 32. Product Database
**Storage:** products.json | **Primary Key:** Barcode (unique) | **Per product:** Barcode, SKU, Name, Brand, Category, Purchase Price, Selling Price, MRP, GST, Stock, Minimum Stock, Supplier, Unit, Weight, Expiry, Batch, HSN, Description

## 33. Cart Engine
**Purpose:** Temporary shopping cart. **Stores:** Selected products, Quantity, Price, Total | **Operations:** Add, Remove, Increase, Decrease, Clear. Totals calculated dynamically

## 34. Billing Engine
**billing.py responsible for:** Subtotal, Tax, Discount, Grand Total. **Future:** Coupons, Multiple GST slabs, Round Off, Service Charges

## 35. PDF Generator
**Uses:** ReportLab | **Produces:** Professional Invoice containing Store Information, Invoice Number, Items, Totals, Barcode, Footer. Automatically saved

## 36. Barcode PDF Engine
**Uses:** ReportLab Code128 | **Supports:** Single Product, All Products, Barcode Range, Custom Layout (Rows, Columns, Product Name, Price, Barcode Number). **Future:** QR Codes, EAN13, UPC

## 37. Hold Bill System
**Purpose:** Pause billing. **Workflow:** Current Cart → Save JSON → Generate Hold Number → Resume Later → Restore Cart. **Used for:** Busy counters, Customer forgot wallet, Pending payments

## 38. Bill History
**Stores:** Every completed bill. **Supports:** Search, View, Reprint, Delete. **Future:** Export, Statistics, Filtering

## 39. Scanner Performance Optimizations
Current optimizations: OpenCV buffer size reduced, ROI scanning, Cooldown timer, Duplicate detection, Frame grabbing, Fast callback, Minimal latency. Significantly improved scanning speed

## 40. Error Handling
Every module attempts to: Catch exceptions, Prevent crashes, Create missing folders, Create missing JSON files, Recover corrupted JSON, Maintain application stability

---

# PART 3: GUI ARCHITECTURE

## 41. GUI Philosophy
Designed for retail shops, grocery stores, medical shops, general stores. Operator should complete billing without mouse. Navigation fast, Large buttons, Minimal popup windows, Professional appearance

## 42. GUI Folder Structure
**gui/ contains:** header.py, toolbar.py, statusbar.py, main_window.py, settings_view.py, product_master.py, splash_screen.py | **Folders:** billing/, dialogs/, payment/, find_bill/, hold_bill/. Each folder groups related windows

## 43. Main Window
**File:** main_window.py | **Role:** Application controller. **Responsibilities:** Creates root window, Loads all views, Handles page switching, Initializes scanner, Initializes toolbar, Creates callbacks, Maintains application state, Coordinates all GUI modules. Should not contain heavy business logic

## 44. Root Window
**Framework:** Tkinter | **Config:** Fullscreen Support, Resizable, Window Icon, Professional Title, Background Color, Application Theme. Escape key exits fullscreen. **Future:** Dark Theme, Theme Switching, Multiple Window Support

## 45. Header
**File:** header.py | **Purpose:** Display application branding (Application Name, Logo, Store Name). **Future:** Logged User, Current Date, Notifications, License Status

## 46. Toolbar
**File:** toolbar.py | **Purpose:** Application Navigation. **Current Buttons:** Billing (New Bill, Save Bill, Print Bill, Hold Bill, Find Bill), Products, Settings, Customers (future), Reports (future), Exit

## 47. Status Bar
**File:** statusbar.py | **Purpose:** Show current status. **Examples:** Ready, Scanner Connected, Scanner Active, Barcode Not Found, Product Added, Current Invoice. **Future:** Memory Usage, Version, Database Status, Internet Status, License Status

## 48. Billing View
**Folder:** billing/ | **Main screen, most frequently used**. **Contains:** Scanner Panel, Manual Barcode Entry, Cart Table, Totals Panel, Generate Bill Button, Clear Cart Button, Hold Bill Button, Scanner Controls. Optimized for cashier operation

## 49. Scanner Panel
**Purpose:** Control barcode scanner. **Functions:** Start Scanner, Stop Scanner, Scanner Status, Manual Barcode Input. **Future:** USB Camera Selection, Resolution, FPS, Camera Test

## 50. Cart Table
**Purpose:** Shows selected products. **Columns:** Product, Quantity, Price, Total | **Functions:** Increase Quantity, Decrease Quantity, Delete Item, Automatic Refresh. **Future:** Discount Per Item, GST Column, Serial Number

## 51. Totals Panel
**Displays:** Subtotal, GST, Discount, Grand Total. **Updates:** Automatically. **Future:** Round Off, Coupon Discount, Loyalty Points

## 52. Payment Dialog
**Folder:** payment/ | **Purpose:** Collect payment. **Current:** Payment Mode, Received Amount, Generate Invoice. **Future:** Cash, UPI, Card, Wallet, Split Payment, Pending Payment

## 53. Product Master
**File:** product_master.py | **Purpose:** Manage products. **Current Features:** Search, Add, Edit, Delete, Print Barcodes, Professional Table. **Future:** Import Excel, Export Excel, Bulk Update, Category Filter

## 54. Product Table
**Columns:** Barcode, SKU, Name, Brand, Category, Stock, Price, GST, Selection | **Single Row Double Click:** Edit Product. **Future:** Sorting, Filtering, Column Resize, Column Hide

## 55. Add Product Dialog
**Folder:** dialogs/ | **Purpose:** Create or edit products. **Stores:** Barcode, SKU, Name, Brand, Category, Purchase Price, Selling Price, MRP, GST, Stock, Minimum Stock, Supplier, Unit, Weight, Expiry, Batch, HSN, Description | **Validation:** Duplicate Barcode, Negative Price, Missing Name. **Future:** Product Image, Category Dropdown, Auto GST

## 56. Barcode Print Dialog
**Purpose:** Generate barcode sheets. **Modes:** Selected Product, All Products, Barcode Range | **Customization:** Rows, Columns, Product Name, Price, Barcode Number | **Output:** PDF. **Future:** QR Codes, Different Label Sizes

## 57. Settings View
**Purpose:** Application configuration. **Current:** Camera URL, Scanner Settings. **Future:** Company Details, Logo, GST, Invoice Prefix, Theme, Backup, Restore

## 58. Find Bill View
**Folder:** find_bill/ | **Purpose:** Search completed invoices. **Current Features:** Search, Refresh, View, Delete, Reprint. **Future:** Date Filter, Customer Filter, Amount Filter, Export

## 59. Bill Details Dialog
**Purpose:** Display invoice. **Shows:** Invoice Number, Date, Items, Quantity, Prices, GST, Total. **Future:** Customer Details, Print Preview

## 60. Hold Bill Window
**Purpose:** Resume previously held bills. **Displays:** Hold Number, Date, Time, Resume, Delete. **Future:** Search

## 61. Splash Screen
**Purpose:** Professional startup. **Shows:** Logo, Loading Progress, Status Message. **Sequence:** Initialize → Database → History → Workspace → Scanner → Launch

## 62. View Switching
**Current Views:** Billing, Products, Settings, Find Bills | **Method:** Hide Current → Show Requested. Only one page visible. Improves performance

## 63. Event System
User Click → GUI Event → Callback → Logic Module → JSON → Response → Refresh GUI. Every interaction follows this flow

## 64. Scanner Events
Scanner → Barcode → Database Search → Product → Cart → Refresh Table → Refresh Totals → Status Update → Ready

## 65. Product Events
**Add:** Validate → Database → Save JSON → Refresh Table | **Edit:** Validate → Save → Refresh | **Delete:** Confirm → Delete → Refresh

## 66. Billing Events
Generate Bill → Payment Dialog → Totals → PDF → History → Reduce Stock → Clear Cart → Next Bill Number

## 67. Error Dialogs
**Current Types:** Information, Warning, Confirmation, Error. Uses messagebox. **Future:** Custom Styled Dialogs

## 68. Current UI Theme
**Primary:** Blue | **Success:** Green | **Danger:** Red | **Warning:** Orange | **Background:** Light Gray | **Widgets:** White | **Fonts:** Segoe UI. Professional appearance

## 69. User Experience Goals
Simple, Fast, Professional, Minimal Clicks, Large Buttons, Readable Tables, Instant Feedback, No unnecessary popups

## 70. Future GUI Improvements
Dashboard, Analytics, Charts, Dark Mode, Ribbon Toolbar, Keyboard Shortcuts, Notification Center, Recent Bills, Customer Module, Reports Module, Multi-language Support, Touch Screen Optimization

---

# PART 4: BUSINESS LOGIC & CORE ENGINE

## 71. Business Logic Layer
**Location:** logic/ | **Purpose:** Contains every backend module. **Responsible for:** Product Database, Billing, Cart, Barcode Scanner, Barcode Generator, PDF Generation, Configuration, Runtime Storage, Bill History, Hold Bills. Contains NO Tkinter UI, GUI simply calls these functions

## 72. Module Overview
**Current modules:** app_dirs.py, app_state.py, barcode_pdf.py, barcode_scanner.py, billing.py, bill_history.py, cart.py, config.py, database.py, file_paths.py, hold_bill.py, pdf_generator.py, resource_path.py

## 73. database.py
**Purpose:** Database layer. **Storage:** products.json | **Responsibilities:** Load products, Save products, Add product, Edit product, Delete product, Search products, Generate invoice numbers, Initialize product database | **Product Structure:** Barcode, SKU, Name, Brand, Category, Purchase Price, Selling Price, MRP, GST, Stock, Minimum Stock, Supplier, Unit, Weight, Expiry, Batch, HSN, Description

## 74. Product Loading
**Startup:** load_products() → products.json exists? → YES: Load JSON → Create dictionary → Ready | NO: Create default product → Save JSON → Ready

## 75. Product Search
**Search Fields:** Barcode, Name, Brand, Category | **Currently:** Case insensitive | **Returns:** Matching product list

## 76. Product CRUD
**Create:** Validate → Save | **Read:** Dictionary Lookup | **Update:** Replace Record → Save JSON | **Delete:** Remove Dictionary Entry → Save JSON

## 77. Bill Number Engine
**Format:** QB-YYYYMMDD-000001 | **Example:** QB-20260806-000001 | **Counter stored in:** bill_counter.json | **Every new invoice:** Counter increases | **Every new day:** Counter resets

## 78. billing.py
**Purpose:** Handles calculations. **Current:** Subtotal, GST, Discount, Grand Total | **Returns:** subtotal, tax, discount, total. Every totals panel refresh uses this module

## 79. Cart Engine
**File:** cart.py | **Purpose:** Temporary shopping cart. **Stores:** Current customer items | **Operations:** Add Item, Remove Item, Update Quantity, Clear Cart. Cart only exists during billing, completed sale clears cart

## 80. Cart Data Structure
**Each cart item contains:** Barcode, Name, Price, Quantity, Total. Total automatically updated

## 81. Add To Cart
Barcode → Database Lookup → Existing Item? → YES: Increase Quantity → Update Total | NO: Create Cart Item → Refresh

## 82. Remove From Cart
User Delete → Remove Item → Refresh Totals → Refresh Table

## 83. Quantity Update
Current Quantity → Increase/Decrease → Quantity <= 0? → YES: Delete Item | NO: Update Total → Refresh

## 84. Barcode Scanner
**File:** barcode_scanner.py | **Uses:** OpenCV, pyzbar, pygame | **Responsibilities:** Camera, Decode Barcode, Cooldown, Duplicate Detection, Scanner Thread, Beep Sound

## 85. Scanner Thread
Runs independently, Main UI never freezes. **Workflow:** Thread → Capture Frame → Decode → Callback → Repeat

## 86. Camera Initialization
**Current Source:** IP Webcam | **Uses:** OpenCV VideoCapture | **Optimizations:** CAP_FFMPEG, Buffer Size, Resolution, FPS, Frame Grab, Reconnect

## 87. Barcode Detection
Frame → Gray Scale → ROI Crop → Decode → Barcode Found → Cooldown Check → Callback

## 88. ROI Optimization
Scanner doesn't decode entire frame, only scans center region. **Advantages:** Faster, Lower CPU, More Stable

## 89. Duplicate Protection
Scanner stores Visible Codes, Last Scan Time. Same barcode cannot continuously trigger. Improves cashier experience

## 90. Scanner Sound
**Current:** beep.mp3 | **Uses:** pygame | **Triggered:** Successful scan only

## 91. barcode_pdf.py
**Purpose:** Generate printable barcode labels. **Uses:** ReportLab, Code128 | **Supports:** Single Product, All Products, Barcode Range, Custom Rows, Custom Columns

## 92. Barcode Layout Engine
**Class:** BarcodeLayout | **Calculates:** Page Width, Margins, Rows, Columns, Label Size, Coordinates. Used for professional printing

## 93. Barcode Label Engine
**Class:** BarcodeLabel | **Draws:** Border, Barcode, Product Name, Price, Barcode Number. Everything centered automatically

## 94. Barcode Generation Flow
Products → Layout → Label → PDF Canvas → barcode_labels.pdf → Open

## 95. PDF Generator
**File:** pdf_generator.py | **Uses:** ReportLab Platypus | **Creates:** Professional invoice

## 96. Invoice Contents
Store Name, Address, Phone, Invoice Number, Invoice Date, Items, Subtotal, GST, Discount, Grand Total, Barcode, Footer

## 97. Font System
**Uses:** DejaVu Fonts | **Reason:** Unicode Support, Rupee Symbol, Reliable PDF Rendering. Fonts packaged with application

## 98. Invoice Storage
**PDF → bills/** | **JSON → bills_history.json**. Both generated together

## 99. Bill History Engine
**File:** bill_history.py | **Purpose:** Read, Search, Return bill history | **Storage:** bills_history.json

## 100. Hold Bill Engine
**File:** hold_bill.py | **Stores:** Temporary carts | **File:** held_bills.json | **Each hold generates:** HB-000001, HB-000002, HB-000003, etc.

## 101. Config Engine
**File:** config.py | **Storage:** config.json | **Current Configuration:** Company, Billing, Scanner. **Future:** Theme, Language, Printer, Database

## 102. Runtime Path System
**Two helper modules:** resource_path.py, data_path() | **Purpose:** Bundled Assets (Read Only), Examples (Fonts, Images, Sounds) | **resource_path() uses:** PyInstaller _MEIPASS

## 103. Writable Data System
**data_path() purpose:** Store runtime files. **Examples:** Products, Bills, History, Config, Barcode PDFs, Invoice PDFs | **Storage Location:** LocalAppData\QuickBill (Professional Windows behaviour)

## 104. Error Recovery
Every module attempts: Create folder, Create JSON, Recover corrupted JSON, Handle exceptions, Prevent application crash, Continue execution whenever possible

## 105. Module Dependency Flow
**GUI → database.py → cart.py → billing.py → pdf_generator.py → bill_history.py → JSON** | **Scanner → database.py → cart.py → GUI Refresh** | **Product Master → database.py → products.json** | **Find Bills → bill_history.py → bills_history.json**

## 106. Thread Safety
**Current background thread:** Barcode Scanner | **Everything else:** Main Tkinter thread. Avoids UI freezing

## 107. Data Persistence
**Persistent Data:** Products, Bills, Settings, History, Counters, Hold Bills | **Temporary Data:** Cart, Scanner Status, Selected Product

## 108. Current Limitations
**Current Version:** Single User, Single Counter, JSON Storage, Windows Only, Offline Only, No Authentication, No Printer API, No Customer Module. Planned for future versions

## 109. Backend Design Principles
One module = One responsibility. No duplicated code. Readable functions. Easy debugging. Minimal dependencies. Easy packaging

---

# PART 5: BUILD, PACKAGING & RELEASE ENGINEERING

## 111. Deployment Philosophy
QuickBill distributed as professional Windows application. End user never needs Python, pip, Git, Visual Studio, Command Prompt. User only downloads QuickBill_Setup_v2.1.0.exe and installs like any commercial Windows software

## 112. Development Environment
**OS:** Windows 11 | **Language:** Python 3.11 | **Package Manager:** pip | **IDE:** Visual Studio Code | **Version Control:** Git | **Repository:** GitHub

## 113. Required Python Packages
**Production packages:** opencv-python, pyzbar, pygame, reportlab, Pillow, pyinstaller, future, numpy. Installed through requirements.txt

## 114. Project Build Process
Development → Python Source → Testing → PyInstaller → QuickBill.exe → Inno Setup → QuickBill_Setup.exe → Release

## 115. PyInstaller
**Purpose:** Convert Python project into executable. **Current Output:** One File - QuickBill.exe | **Advantages:** Simple distribution, No Python installation required, Professional deployment

## 116. QuickBill.spec
**Purpose:** Controls executable generation. **Responsibilities:** Application name, Application icon, Version resource, Bundled assets, Hidden imports, DLL inclusion, ReportLab data, pyzbar libraries

## 117. Bundled Assets
PyInstaller includes assets/ containing Fonts, Images, Sounds, Logo. Become read-only resources, Loaded using resource_path()

## 118. Hidden Imports
**Current hidden modules:** ReportLab, pyzbar | **Reason:** PyInstaller cannot automatically detect every dynamic import. Therefore collect_submodules() used

## 119. External DLLs
**Current DLLs:** libzbar-64.dll, libiconv.dll | **Purpose:** Barcode decoding | **Bundled:** Manually into executable

## 120. Version Information
QuickBill includes Windows VERSIONINFO containing Company, Product Name, Description, Copyright, Version, Original Filename. Appears in File Properties, Windows Explorer, Task Manager

## 121. Application Icon
**Current icon:** logo.ico | **Used in:** Executable, Window, Taskbar, Installer, Desktop Shortcut, Start Menu Shortcut. Single source icon

## 122. Runtime Resource System
**resource_path():** Loads bundled resources (Fonts, Images, Icons, Sounds) - Read Only | **data_path():** Loads runtime files (Products, Bills, History, Configuration, Counters, Barcode PDFs, Invoice PDFs) - Read Write

## 123. Runtime Data Folder
**Stored in:** LocalAppData\QuickBill | **Contains:** products.json, config.json, bill_counter.json, held_bills.json, bills_history.json, bills/, barcodes/ | **Advantages:** No Administrator Rights, Cleaner installation, Professional behaviour, Easy updates

## 124. First Launch
**On first startup:** QuickBill automatically creates LocalAppData → QuickBill → Required folders → Required JSON files → Default configuration. User never needs to create files manually

## 125. Folder Creation
**Automatically created folders:** bills/, barcodes/ | **Automatically created JSON:** products.json, config.json, bill_counter.json, held_bills.json, bills_history.json. Application always checks existence before use

## 126. Installer
**Current installer:** Inno Setup | **Wizard Style:** Modern | **Compression:** LZMA2 Solid Compression Enabled | **Produces:** Professional Windows installer

## 127. Installer Features
**Current Features:** Welcome Screen, License Agreement, Installation Folder, Desktop Shortcut, Start Menu Shortcut, Application Icon, Professional Wizard, Progress Bar, Finish Screen, Uninstaller

## 128. Installer Information
**Current metadata:** Application Name, Version, Publisher, Description, Copyright, Architecture, Output Filename, Application Directory

## 129. Installation Directory
**Default:** Program Files\QuickBill. Application files remain here, User data does NOT

## 130. User Data Directory
**Default:** LocalAppData\QuickBill | **Advantages:** User files survive application updates, Professional Windows standard

## 131. Uninstaller
**Automatically generated by:** Inno Setup | **Capabilities:** Remove executable, Remove shortcuts, Remove Start Menu entries, Registered inside Windows Apps & Features. Professional uninstall experience

## 132. Installer Compression
**Current:** LZMA2 Solid Compression | **Purpose:** Reduce installer size, Faster downloads, Professional distribution

## 133. Release Folder
**Current structure:** release/ | **Contains:** Final Setup Executable, Ready for distribution. Nothing else should be placed here

## 134. Git Repository
**Stores:** Source Code, Assets, Specification Files, Installer Scripts, Documentation | **Does NOT permanently store:** Generated executable, Temporary build folders, User runtime data

## 135. Ignored Files
**Git ignores:** build/, dist/, __pycache__/, Local runtime files, Generated PDFs, Generated barcode sheets. Keeps repository clean

## 136. Release Checklist
**Before release:** ✓ Update version, ✓ Test application, ✓ Build executable, ✓ Test executable, ✓ Build installer, ✓ Test installer, ✓ Test uninstall, ✓ Verify icons, ✓ Verify version info, ✓ Push source code, ✓ Upload installer

## 137. Version Upgrade Procedure
Increase version number → Update VERSIONINFO → Update Installer Version → Rebuild EXE → Rebuild Installer → Test → Release

## 138. Testing Checklist
Application starts, Scanner works, Products load, Products save, Bills generate, PDF opens, Barcode PDF works, History works, Hold Bill works, Settings save, Installer installs, Uninstaller removes, Desktop shortcut works, Start Menu works

## 139. Known Design Decisions
**JSON chosen instead of SQLite:** Simple, Portable, Readable, Offline, Easy backup | **Tkinter selected because:** Lightweight, Native, Fast, No web runtime required

## 140. Future Release Goals
**Version 2.x:** Customer Module, Reports, Sales Dashboard, Dark Theme, Printer Integration | **Version 3.x:** SQLite Database, Authentication, Employee Accounts, Backup Manager, Cloud Sync, Analytics, GST Reports, Multi-terminal Support

## 141. Long-Term Vision
QuickBill intended to evolve into complete retail ERP. **Future modules:** Customers, Suppliers, Purchase Orders, Expense Tracking, Sales Reports, Profit Analysis, Inventory Analytics, GST Reports, Thermal Printer Support, Receipt Designer, Barcode Scanner Configuration, Automatic Backup, Cloud Synchronization, Role-Based Access, License Activation, Plugin System

## 142. Development Principles
Every new feature should: Follow existing folder structure, Remain modular, Avoid duplicated code, Use helper functions, Separate UI and logic, Preserve backward compatibility, Maintain offline-first design

## 143. Project Status
**Current Version:** v2.1.0 | **Status:** Production Ready | **Application:** Stable | **Installer:** Stable | **Packaging:** Stable | **Runtime Storage:** Stable | **PDF Generation:** Stable | **Barcode System:** Stable | Ready for future feature development
