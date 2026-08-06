# QuickBill
# Complete Project Context
# Version 2.0.0

---

# 1. Project Information

Project Name:
QuickBill

Current Version:
v2.0.0

Project Type:
Desktop Billing & Inventory Management Software

Language:
Python 3.11

Operating System:
Windows

UI Framework:
Tkinter

License:
MIT License

Packaging:
PyInstaller

Installer:
Inno Setup

Repository:
https://github.com/kartikbansode/quickbill

---

# 2. Project Goal

QuickBill is a complete desktop billing software created for small businesses,
retail shops, grocery stores and local stores.

The objective is to provide a lightweight but professional billing system
without requiring any internet connection or external database.

The application stores all data locally.

Everything is designed to be simple, fast and professional.

---

# 3. Design Philosophy

The project follows these principles.

• Lightweight
• Offline First
• Fast Startup
• Professional UI
• Easy Maintenance
• Modular Architecture
• No unnecessary dependencies
• Easy future expansion

Every module should perform only one responsibility.

Business logic should never be mixed with UI whenever possible.

---

# 4. Current Version

Version:
2.0.0

Current Status:
Stable

Major Milestone:
Professional Windows Desktop Application

Completed Features:

✓ Billing System

✓ Product Management

✓ Barcode Scanner

✓ Barcode Label Generator

✓ PDF Invoice Generator

✓ Hold Bills

✓ Bill History

✓ Search Bills

✓ Settings

✓ Installer

✓ Uninstaller

✓ Version Information

✓ Runtime Data Storage

✓ Professional Packaging

---

# 5. Technology Stack

Programming Language

Python 3.11

GUI

Tkinter

PDF Generation

ReportLab

Barcode Generation

ReportLab Code128

Barcode Reading

pyzbar

Camera

OpenCV

Sound

pygame

Packaging

PyInstaller

Installer

Inno Setup

Version Resource

Windows VERSIONINFO

Icons

ICO

Fonts

DejaVu Font Family

Storage

JSON Files

---

# 6. Project Structure

Root

QuickBill/

Contains complete project.

Main folders

assets/
gui/
logic/
installer/
licenses/
version/

Main files

app.py

QuickBill.spec

requirements.txt

README.md

LICENSE

.gitignore

PROJECT_CONTEXT.md

---

# 7. assets/

Purpose

Stores every static resource required by the application.

Subfolders

fonts/

Contains all DejaVu fonts.

Reason:

PDF generation must work even if the system doesn't have the fonts installed.

images/

Contains

logo.png

logo.ico

These are used by

Application icon

Installer

Taskbar

Window icon

sounds/

Contains

beep.mp3

Used by

Barcode scanner successful scan sound.

---

# 8. gui/

Purpose

Contains every user interface component.

The GUI never directly manipulates files.

It always calls functions inside logic/.

GUI is only responsible for

Displaying data

Receiving user input

Calling business logic

Updating interface

---

Subfolders

billing/

Contains billing related widgets.

dialogs/

Popup dialogs.

payment/

Payment window.

find_bill/

Bill history interface.

hold_bill/

Hold bill window.

---

Main GUI Files

main_window.py

Main application.

Acts as controller.

Creates

Toolbar

Header

Billing View

Product View

Settings

Bill History

Status Bar

Routes all user actions.

header.py

Application header.

toolbar.py

Top navigation.

statusbar.py

Bottom status information.

product_master.py

Complete product management interface.

settings_view.py

Application settings.

splash_screen.py

Loading screen.

---

# 9. logic/

Purpose

Contains business logic.

This folder must never contain UI code.

Everything inside logic can be reused without Tkinter.

Modules

database.py

Product database.

CRUD operations.

JSON storage.

config.py

Application settings.

cart.py

Shopping cart logic.

billing.py

Price calculations.

barcode_scanner.py

Camera scanning.

barcode_pdf.py

Barcode sheet generation.

pdf_generator.py

Invoice generation.

bill_history.py

Bill search.

hold_bill.py

Hold functionality.

resource_path.py

Access bundled assets.

app_dirs.py

Application runtime directory.

---

# 10. Runtime Data

QuickBill separates

Application files

from

User files.

Application files

Executable

Assets

Fonts

Images

Installer

These never change.

User files

Products

Bills

History

Config

Barcode PDFs

Generated invoices

These are writable.

---

# 11. Runtime Storage

All writable files are stored in

LocalAppData

instead of beside the executable.

Reason

Program Files

is read-only for normal users.

LocalAppData

does not require administrator permission.

Benefits

Cleaner installation

Safer updates

Professional behavior

Same as commercial Windows applications.

---

# 12. Resource System

Two different path systems exist.

resource_path()

Purpose

Load bundled assets.

Examples

Fonts

Images

Icons

Sounds

Logo

These resources are packaged into the executable.

They are read-only.

---

data_path()

Purpose

Load writable data.

Examples

products.json

config.json

bill_counter.json

held_bills.json

bills_history.json

Generated PDFs

Generated barcode sheets

This folder is automatically created on first launch.

---

# 13. JSON Database

QuickBill intentionally avoids SQLite.

Reason

Simple

Portable

Human readable

Easy backup

Easy restore

Easy debugging

Current JSON files

products.json

Stores all products.

config.json

Stores application settings.

bill_counter.json

Stores invoice counter.

held_bills.json

Stores held bills.

bills_history.json

Stores completed bills.

---

# 14. Build System

Development

python app.py

Production

PyInstaller

Spec file

QuickBill.spec

Output

dist/

Contains

QuickBill.exe

One-file executable.

Professional Windows application.

---

# 15. Installer

Installer Technology

Inno Setup

Capabilities

Professional wizard

Desktop shortcut

Start Menu shortcut

Uninstaller

Version information

License

Company information

Application icon

Modern wizard style

Compression enabled

Professional installation experience.

---

# 16. Coding Standards

Naming

snake_case

Classes

PascalCase

Constants

UPPER_CASE

Indentation

4 spaces

Encoding

UTF-8

All paths should use helper functions.

Hardcoded file paths should never be used.

---

# ==========================================================
# PART 2
# APPLICATION ARCHITECTURE
# ==========================================================

# 17. Overall Software Architecture

QuickBill follows a layered architecture.

The application is divided into three major layers.

--------------------------------------------------

Presentation Layer

↓

Business Logic Layer

↓

Data Layer

--------------------------------------------------

Presentation Layer

Location

gui/

Responsible for

Displaying windows

Taking user input

Rendering tables

Showing dialogs

Updating UI

Never performs

File writing

Database operations

Calculations

Business decisions

Instead it calls functions inside logic/.

--------------------------------------------------

Business Logic Layer

Location

logic/

Responsible for

Calculations

Barcode processing

Database operations

Invoice generation

Cart management

Configuration

This layer contains all application rules.

It should remain independent of Tkinter.

--------------------------------------------------

Data Layer

Storage Type

JSON

Purpose

Store

Products

Bills

Settings

History

Counters

Held Bills

Advantages

Easy backup

Easy migration

Easy editing

No installation required

Portable

--------------------------------------------------

# 18. Startup Flow

Application starts from

app.py

Execution order

main()

↓

Splash Screen

↓

Initialize Product Database

↓

Initialize Bill Database

↓

Prepare Runtime Environment

↓

Load Configuration

↓

Initialize Scanner

↓

Launch Main Window

↓

Application Ready

--------------------------------------------------

# 19. app.py

Purpose

Entry point of QuickBill.

Responsibilities

Display splash screen

Initialize databases

Load runtime

Start main window

Nothing else.

Business logic should never be placed here.

--------------------------------------------------

# 20. Splash Screen

Purpose

Professional startup experience.

Current Progress Sequence

10%

Initializing QuickBill

30%

Loading Product Database

55%

Loading Billing History

75%

Preparing Workspace

90%

Initializing Barcode Scanner

100%

Launching Application

Once complete

Splash closes.

Main window opens.

--------------------------------------------------

# 21. Main Window

main_window.py

This is the application controller.

Every major component is created here.

Components

Header

Toolbar

Billing View

Product Master

Settings

Bill History

Status Bar

Payment Dialog

Hold Bill Window

Barcode Scanner

This file controls navigation.

It should not contain database code.

--------------------------------------------------

# 22. Navigation System

Toolbar buttons

↓

Corresponding View

↓

Hide Previous View

↓

Show Requested View

Only one major page is visible.

Views

Billing

Products

Settings

Find Bills

Future

Reports

Customers

Analytics

--------------------------------------------------

# 23. Billing Workflow

Customer arrives

↓

Cashier scans barcode

↓

Scanner returns barcode

↓

Database searches product

↓

Product found

↓

Add to cart

↓

Refresh totals

↓

Generate bill

↓

Payment dialog

↓

Generate PDF

↓

Reduce stock

↓

Save history

↓

Clear cart

↓

Generate next invoice

--------------------------------------------------

# 24. Product Workflow

Open Product Master

↓

Search

↓

Edit

↓

Save

↓

Update JSON

↓

Refresh Table

↓

Ready

Add Product

↓

Validate Data

↓

Save JSON

↓

Refresh Table

Delete Product

↓

Confirmation

↓

Remove JSON

↓

Refresh Table

--------------------------------------------------

# 25. Barcode Scanner Workflow

Camera

↓

OpenCV

↓

Frame

↓

Convert Gray

↓

Crop ROI

↓

pyzbar Decode

↓

Barcode Found

↓

Cooldown Check

↓

Callback

↓

Database Search

↓

Add Product

↓

Play Sound

↓

Refresh Cart

Scanner prevents

Duplicate scans

False reads

Continuous spam

--------------------------------------------------

# 26. Barcode Generator Workflow

User

↓

Product Master

↓

Print Barcode

↓

Barcode Dialog

↓

Select Products

↓

Generate Labels

↓

ReportLab

↓

barcode_labels.pdf

↓

Open Automatically

--------------------------------------------------

# 27. Invoice Workflow

Cart Ready

↓

Payment

↓

Generate Invoice Number

↓

Calculate Totals

↓

Create PDF

↓

Save JSON

↓

Reduce Stock

↓

History Updated

↓

Cart Cleared

--------------------------------------------------

# 28. Runtime Data Flow

Scanner

↓

Database

↓

Cart

↓

Billing Engine

↓

PDF Generator

↓

History

↓

User

Every module performs one task.

No duplicated responsibilities.

--------------------------------------------------

# 29. Module Communication

GUI

↓

logic.database

↓

logic.cart

↓

logic.billing

↓

logic.pdf_generator

↓

JSON Files

The GUI never directly edits JSON.

Only logic modules perform file operations.

--------------------------------------------------

# 30. Resource Loading

Bundled Assets

↓

resource_path()

Runtime Data

↓

data_path()

Never mix both.

Assets are read-only.

Runtime data is writable.

--------------------------------------------------

# 31. Configuration System

config.json

Stores

Company Name

Owner

GST

Phone

Email

Logo

Currency

Tax

Discount

Scanner URL

Scanner Type

Scanner Delay

Scanner Beep

Future settings should also be stored here.

--------------------------------------------------

# 32. Product Database

Current Storage

products.json

Primary Key

Barcode

Each product stores

Barcode

SKU

Name

Brand

Category

Purchase Price

Selling Price

MRP

GST

Stock

Minimum Stock

Supplier

Unit

Weight

Expiry

Batch

HSN

Description

Barcode is unique.

--------------------------------------------------

# 33. Cart Engine

Purpose

Temporary shopping cart.

Stores

Selected products

Quantity

Price

Total

Operations

Add

Remove

Increase

Decrease

Clear

Totals are calculated dynamically.

--------------------------------------------------

# 34. Billing Engine

billing.py

Responsible for

Subtotal

Tax

Discount

Grand Total

Future

Coupons

Multiple GST slabs

Round Off

Service Charges

--------------------------------------------------

# 35. PDF Generator

Uses

ReportLab

Produces

Professional Invoice

Contains

Store Information

Invoice Number

Items

Totals

Barcode

Footer

Automatically saved.

--------------------------------------------------

# 36. Barcode PDF Engine

Uses

ReportLab

Code128

Supports

Single Product

All Products

Barcode Range

Custom Layout

Rows

Columns

Product Name

Price

Barcode Number

Future support

QR Codes

EAN13

UPC

--------------------------------------------------

# 37. Hold Bill System

Purpose

Pause billing.

Workflow

Current Cart

↓

Save JSON

↓

Generate Hold Number

↓

Resume Later

↓

Restore Cart

Used for

Busy counters

Customer forgot wallet

Pending payments

--------------------------------------------------

# 38. Bill History

Stores

Every completed bill.

Supports

Search

View

Reprint

Delete

Future

Export

Statistics

Filtering

--------------------------------------------------

# 39. Scanner Performance Optimizations

Current Optimizations

OpenCV buffer size reduced

ROI scanning

Cooldown timer

Duplicate detection

Frame grabbing

Fast callback

Minimal latency

These changes significantly improved scanning speed.

--------------------------------------------------

# 40. Error Handling

Every module attempts to

Catch exceptions

Prevent crashes

Create missing folders

Create missing JSON files

Recover corrupted JSON

Maintain application stability.

--------------------------------------------------

# ==========================================================
# PART 3
# GUI ARCHITECTURE
# ==========================================================

# 41. GUI Philosophy

QuickBill follows a simple desktop ERP style interface.

The interface is designed for

• Retail Shops
• Grocery Stores
• Medical Shops
• General Stores

The operator should be able to complete billing without using the mouse whenever possible.

Navigation should feel fast.

Large buttons.

Minimal popup windows.

Professional appearance.

--------------------------------------------------

# 42. GUI Folder Structure

gui/

Contains every visual component.

Files

header.py
toolbar.py
statusbar.py
main_window.py
settings_view.py
product_master.py
splash_screen.py

Folders

billing/

dialogs/

payment/

find_bill/

hold_bill/

Each folder groups related windows together.

--------------------------------------------------

# 43. Main Window

File

main_window.py

Purpose

Acts as the application controller.

Responsibilities

Creates root window.

Loads all views.

Handles page switching.

Initializes scanner.

Initializes toolbar.

Creates callbacks.

Maintains application state.

Coordinates all GUI modules.

No heavy business logic should exist here.

--------------------------------------------------

# 44. Root Window

Current Framework

Tkinter

Configuration

Fullscreen Support

Resizable

Window Icon

Professional Title

Background Color

Application Theme

Escape key exits fullscreen.

Future

Dark Theme

Theme Switching

Multiple Window Support

--------------------------------------------------

# 45. Header

File

header.py

Purpose

Display application branding.

Usually contains

Application Name

Logo

Store Name

Future

Logged User

Current Date

Notifications

License Status

--------------------------------------------------

# 46. Toolbar

File

toolbar.py

Purpose

Application Navigation.

Current Buttons

Billing

New Bill

Save Bill

Print Bill

Hold Bill

Find Bill

Products

Settings

Customers

Reports

Exit

Current

Customers

Reports

Reserved for future.

--------------------------------------------------

# 47. Status Bar

File

statusbar.py

Purpose

Shows current application status.

Examples

Ready

Scanner Connected

Scanner Active

Barcode Not Found

Product Added

Current Invoice

Future

Memory Usage

Version

Database Status

Internet Status

License Status

--------------------------------------------------

# 48. Billing View

Folder

billing/

Main screen.

Most frequently used page.

Contains

Scanner Panel

Manual Barcode Entry

Cart Table

Totals Panel

Generate Bill Button

Clear Cart Button

Hold Bill Button

Scanner Controls

This screen is optimized for cashier operation.

--------------------------------------------------

# 49. Scanner Panel

Purpose

Control barcode scanner.

Functions

Start Scanner

Stop Scanner

Scanner Status

Manual Barcode Input

Future

USB Camera Selection

Resolution

FPS

Camera Test

--------------------------------------------------

# 50. Cart Table

Purpose

Shows all selected products.

Columns

Product

Quantity

Price

Total

Functions

Increase Quantity

Decrease Quantity

Delete Item

Automatic Refresh

Future

Discount Per Item

GST Column

Serial Number

--------------------------------------------------

# 51. Totals Panel

Displays

Subtotal

GST

Discount

Grand Total

Updates

Automatically.

Future

Round Off

Coupon Discount

Loyalty Points

--------------------------------------------------

# 52. Payment Dialog

Folder

payment/

Purpose

Collect payment.

Current

Payment Mode

Received Amount

Generate Invoice

Future

Cash

UPI

Card

Wallet

Split Payment

Pending Payment

--------------------------------------------------

# 53. Product Master

File

product_master.py

Purpose

Manage products.

Current Features

Search

Add

Edit

Delete

Print Barcodes

Professional Table

Future

Import Excel

Export Excel

Bulk Update

Category Filter

--------------------------------------------------

# 54. Product Table

Columns

Barcode

SKU

Name

Brand

Category

Stock

Price

GST

Selection

Single Row

Double Click

Edit Product

Future

Sorting

Filtering

Column Resize

Column Hide

--------------------------------------------------

# 55. Add Product Dialog

Folder

dialogs/

Purpose

Create or edit products.

Stores

Barcode

SKU

Name

Brand

Category

Purchase Price

Selling Price

MRP

GST

Stock

Minimum Stock

Supplier

Unit

Weight

Expiry

Batch

HSN

Description

Validation

Duplicate Barcode

Negative Price

Missing Name

Future

Product Image

Category Dropdown

Auto GST

--------------------------------------------------

# 56. Barcode Print Dialog

Purpose

Generate barcode sheets.

Modes

Selected Product

All Products

Barcode Range

Customization

Rows

Columns

Product Name

Price

Barcode Number

Output

PDF

Future

QR Codes

Different Label Sizes

--------------------------------------------------

# 57. Settings View

Purpose

Application configuration.

Current

Camera URL

Scanner Settings

Future

Company Details

Logo

GST

Invoice Prefix

Theme

Backup

Restore

--------------------------------------------------

# 58. Find Bill View

Folder

find_bill/

Purpose

Search completed invoices.

Current Features

Search

Refresh

View

Delete

Reprint

Future

Date Filter

Customer Filter

Amount Filter

Export

--------------------------------------------------

# 59. Bill Details Dialog

Purpose

Display invoice.

Shows

Invoice Number

Date

Items

Quantity

Prices

GST

Total

Future

Customer Details

Print Preview

--------------------------------------------------

# 60. Hold Bill Window

Purpose

Resume previously held bills.

Displays

Hold Number

Date

Time

Resume

Delete

Future

Search

--------------------------------------------------

# 61. Splash Screen

Purpose

Professional startup.

Shows

Logo

Loading Progress

Status Message

Current Sequence

Initialize

Database

History

Workspace

Scanner

Launch

--------------------------------------------------

# 62. View Switching

Current Views

Billing

Products

Settings

Find Bills

Navigation Method

Hide Current

↓

Show Requested

Only one page remains visible.

Improves performance.

--------------------------------------------------

# 63. Event System

User Click

↓

GUI Event

↓

Callback

↓

Logic Module

↓

JSON

↓

Response

↓

Refresh GUI

Every interaction follows this flow.

--------------------------------------------------

# 64. Scanner Events

Scanner

↓

Barcode

↓

Database Search

↓

Product

↓

Cart

↓

Refresh Table

↓

Refresh Totals

↓

Status Update

↓

Ready

--------------------------------------------------

# 65. Product Events

Add

↓

Validate

↓

Database

↓

Save JSON

↓

Refresh Table

Edit

↓

Validate

↓

Save

↓

Refresh

Delete

↓

Confirm

↓

Delete

↓

Refresh

--------------------------------------------------

# 66. Billing Events

Generate Bill

↓

Payment Dialog

↓

Totals

↓

PDF

↓

History

↓

Reduce Stock

↓

Clear Cart

↓

Next Bill Number

--------------------------------------------------

# 67. Error Dialogs

Current Dialog Types

Information

Warning

Confirmation

Error

Uses

messagebox

Future

Custom Styled Dialogs

--------------------------------------------------

# 68. Current UI Theme

Primary

Blue

Success

Green

Danger

Red

Warning

Orange

Background

Light Gray

Widgets

White

Fonts

Segoe UI

Professional appearance.

--------------------------------------------------

# 69. User Experience Goals

Simple

Fast

Professional

Minimal Clicks

Large Buttons

Readable Tables

Instant Feedback

No unnecessary popups.

--------------------------------------------------

# 70. Future GUI Improvements

Dashboard

Analytics

Charts

Dark Mode

Ribbon Toolbar

Keyboard Shortcuts

Notification Center

Recent Bills

Customer Module

Reports Module

Multi-language Support

Touch Screen Optimization

--------------------------------------------------


# ==========================================================
# PART 4
# BUSINESS LOGIC & CORE ENGINE
# ==========================================================

# 71. Business Logic Layer

Location

logic/

Purpose

The logic folder contains every backend module used by QuickBill.

It is responsible for

• Product Database
• Billing
• Cart
• Barcode Scanner
• Barcode Generator
• PDF Generation
• Configuration
• Runtime Storage
• Bill History
• Hold Bills

The logic layer contains NO Tkinter UI.

GUI simply calls these functions.

--------------------------------------------------

# 72. Module Overview

Current modules

app_dirs.py

app_state.py

barcode_pdf.py

barcode_scanner.py

billing.py

bill_history.py

cart.py

config.py

database.py

file_paths.py

hold_bill.py

pdf_generator.py

resource_path.py

--------------------------------------------------

# 73. database.py

Purpose

Acts as the application's database layer.

Storage

products.json

Responsibilities

Load products

Save products

Add product

Edit product

Delete product

Search products

Generate invoice numbers

Initialize product database

Current Product Structure

Barcode

SKU

Name

Brand

Category

Purchase Price

Selling Price

MRP

GST

Stock

Minimum Stock

Supplier

Unit

Weight

Expiry

Batch

HSN

Description

--------------------------------------------------

# 74. Product Loading

Application Startup

↓

load_products()

↓

products.json exists?

↓

YES

↓

Load JSON

↓

Create dictionary

↓

Ready

NO

↓

Create default product

↓

Save JSON

↓

Ready

--------------------------------------------------

# 75. Product Search

Search Fields

Barcode

Name

Brand

Category

Search is currently

Case insensitive.

Returns

Matching product list.

--------------------------------------------------

# 76. Product CRUD

Create

↓

Validate

↓

Save

Read

↓

Dictionary Lookup

Update

↓

Replace Record

↓

Save JSON

Delete

↓

Remove Dictionary Entry

↓

Save JSON

--------------------------------------------------

# 77. Bill Number Engine

Current Format

QB-YYYYMMDD-000001

Example

QB-20260806-000001

Counter stored in

bill_counter.json

Every new invoice

Counter increases.

Every new day

Counter resets.

--------------------------------------------------

# 78. billing.py

Purpose

Handles calculations.

Current calculations

Subtotal

GST

Discount

Grand Total

Returns

subtotal

tax

discount

total

Every totals panel refresh uses this module.

--------------------------------------------------

# 79. Cart Engine

File

cart.py

Purpose

Temporary shopping cart.

Stores

Current customer items.

Operations

Add Item

Remove Item

Update Quantity

Clear Cart

Cart only exists during billing.

Completed sale clears cart.

--------------------------------------------------

# 80. Cart Data Structure

Each cart item contains

Barcode

Name

Price

Quantity

Total

Total

Automatically updated.

--------------------------------------------------

# 81. Add To Cart

Barcode

↓

Database Lookup

↓

Existing Item?

↓

YES

Increase Quantity

↓

Update Total

NO

↓

Create Cart Item

↓

Refresh

--------------------------------------------------

# 82. Remove From Cart

User Delete

↓

Remove Item

↓

Refresh Totals

↓

Refresh Table

--------------------------------------------------

# 83. Quantity Update

Current Quantity

↓

Increase / Decrease

↓

Quantity <= 0 ?

↓

YES

Delete Item

NO

↓

Update Total

↓

Refresh

--------------------------------------------------

# 84. Barcode Scanner

File

barcode_scanner.py

Uses

OpenCV

pyzbar

pygame

Responsibilities

Camera

Decode Barcode

Cooldown

Duplicate Detection

Scanner Thread

Beep Sound

--------------------------------------------------

# 85. Scanner Thread

Runs independently.

Main UI never freezes.

Workflow

Thread

↓

Capture Frame

↓

Decode

↓

Callback

↓

Repeat

--------------------------------------------------

# 86. Camera Initialization

Current Source

IP Webcam

Uses

OpenCV VideoCapture

Optimizations

CAP_FFMPEG

Buffer Size

Resolution

FPS

Frame Grab

Reconnect

--------------------------------------------------

# 87. Barcode Detection

Frame

↓

Gray Scale

↓

ROI Crop

↓

Decode

↓

Barcode Found

↓

Cooldown Check

↓

Callback

--------------------------------------------------

# 88. ROI Optimization

Scanner does not decode

Entire Frame.

Only scans

Center region.

Advantages

Faster

Lower CPU

More Stable

--------------------------------------------------

# 89. Duplicate Protection

Scanner stores

Visible Codes

Last Scan Time

Same barcode

Cannot continuously trigger.

Improves cashier experience.

--------------------------------------------------

# 90. Scanner Sound

Current

beep.mp3

Uses

pygame

Triggered

Successful scan only.

--------------------------------------------------

# 91. barcode_pdf.py

Purpose

Generate printable barcode labels.

Uses

ReportLab

Code128

Supports

Single Product

All Products

Barcode Range

Custom Rows

Custom Columns

--------------------------------------------------

# 92. Barcode Layout Engine

Class

BarcodeLayout

Calculates

Page Width

Margins

Rows

Columns

Label Size

Coordinates

Used for

Professional printing.

--------------------------------------------------

# 93. Barcode Label Engine

Class

BarcodeLabel

Draws

Border

Barcode

Product Name

Price

Barcode Number

Everything is centered automatically.

--------------------------------------------------

# 94. Barcode Generation Flow

Products

↓

Layout

↓

Label

↓

PDF Canvas

↓

barcode_labels.pdf

↓

Open

--------------------------------------------------

# 95. PDF Generator

File

pdf_generator.py

Uses

ReportLab Platypus

Creates

Professional invoice.

--------------------------------------------------

# 96. Invoice Contents

Store Name

Address

Phone

Invoice Number

Invoice Date

Items

Subtotal

GST

Discount

Grand Total

Barcode

Footer

--------------------------------------------------

# 97. Font System

Uses

DejaVu Fonts

Reason

Unicode Support

Rupee Symbol

Reliable PDF Rendering

Fonts packaged with application.

--------------------------------------------------

# 98. Invoice Storage

PDF

↓

bills/

JSON

↓

bills_history.json

Both generated together.

--------------------------------------------------

# 99. Bill History Engine

File

bill_history.py

Purpose

Read

Search

Return

Bill history.

Storage

bills_history.json

--------------------------------------------------

# 100. Hold Bill Engine

File

hold_bill.py

Stores

Temporary carts.

File

held_bills.json

Each hold generates

HB-000001

HB-000002

HB-000003

etc.

--------------------------------------------------

# 101. Config Engine

File

config.py

Storage

config.json

Current Configuration

Company

Billing

Scanner

Future

Theme

Language

Printer

Database

--------------------------------------------------

# 102. Runtime Path System

Two helper modules

resource_path.py

data_path()

Purpose

Bundled Assets

Read Only

Examples

Fonts

Images

Sounds

resource_path()

Uses

PyInstaller _MEIPASS

--------------------------------------------------

# 103. Writable Data System

data_path()

Purpose

Store runtime files.

Examples

Products

Bills

History

Config

Barcode PDFs

Invoice PDFs

Storage Location

LocalAppData

QuickBill

Professional Windows behaviour.

--------------------------------------------------

# 104. Error Recovery

Every module attempts

Create folder

Create JSON

Recover corrupted JSON

Handle exceptions

Prevent application crash

Continue execution whenever possible.

--------------------------------------------------

# 105. Module Dependency Flow

GUI

↓

database.py

↓

cart.py

↓

billing.py

↓

pdf_generator.py

↓

bill_history.py

↓

JSON

Scanner

↓

database.py

↓

cart.py

↓

GUI Refresh

Product Master

↓

database.py

↓

products.json

Find Bills

↓

bill_history.py

↓

bills_history.json

--------------------------------------------------

# 106. Thread Safety

Current background thread

Barcode Scanner

Everything else runs

Main Tkinter thread.

Avoids UI freezing.

--------------------------------------------------

# 107. Data Persistence

Persistent Data

Products

Bills

Settings

History

Counters

Hold Bills

Temporary Data

Cart

Scanner Status

Selected Product

--------------------------------------------------

# 108. Current Limitations

Current Version

Single User

Single Counter

JSON Storage

Windows Only

Offline Only

No Authentication

No Printer API

No Customer Module

These are planned for future versions.

--------------------------------------------------

# 109. Backend Design Principles

One module

One responsibility.

No duplicated code.

Readable functions.

Easy debugging.

Minimal dependencies.

Easy packaging.

--------------------------------------------------

# ==========================================================
# PART 5
# BUILD, PACKAGING & RELEASE ENGINEERING
# ==========================================================

# 111. Deployment Philosophy

QuickBill is distributed as a professional Windows application.

The end user should never need to install

Python

pip

Git

Visual Studio

Command Prompt

The user only downloads

QuickBill_Setup_v2.0.0.exe

and installs it like any commercial Windows software.

--------------------------------------------------

# 112. Development Environment

Operating System

Windows 11

Language

Python 3.11

Package Manager

pip

IDE

Visual Studio Code

Version Control

Git

Repository

GitHub

--------------------------------------------------

# 113. Required Python Packages

Current production packages

opencv-python

pyzbar

pygame

reportlab

Pillow

pyinstaller

future

numpy

These packages are installed through

requirements.txt

--------------------------------------------------

# 114. Project Build Process

Development

↓

Python Source

↓

Testing

↓

PyInstaller

↓

QuickBill.exe

↓

Inno Setup

↓

QuickBill_Setup.exe

↓

Release

--------------------------------------------------

# 115. PyInstaller

Purpose

Convert Python project into executable.

Current Output

One File

QuickBill.exe

Advantages

Simple distribution

No Python installation required

Professional deployment

--------------------------------------------------

# 116. QuickBill.spec

Purpose

Controls executable generation.

Responsibilities

Application name

Application icon

Version resource

Bundled assets

Hidden imports

DLL inclusion

ReportLab data

pyzbar libraries

--------------------------------------------------

# 117. Bundled Assets

PyInstaller includes

assets/

Inside assets

Fonts

Images

Sounds

Logo

These become read-only resources.

Loaded using

resource_path()

--------------------------------------------------

# 118. Hidden Imports

Current hidden modules

ReportLab

pyzbar

Reason

PyInstaller cannot automatically detect every dynamic import.

Therefore

collect_submodules()

is used.

--------------------------------------------------

# 119. External DLLs

Current DLLs

libzbar-64.dll

libiconv.dll

Purpose

Barcode decoding.

Bundled manually into executable.

--------------------------------------------------

# 120. Version Information

QuickBill includes Windows VERSIONINFO.

Contains

Company

Product Name

Description

Copyright

Version

Original Filename

This information appears inside

File Properties

Windows Explorer

Task Manager

--------------------------------------------------

# 121. Application Icon

Current icon

logo.ico

Used in

Executable

Window

Taskbar

Installer

Desktop Shortcut

Start Menu Shortcut

Single source icon.

--------------------------------------------------

# 122. Runtime Resource System

Two path helpers exist.

resource_path()

Loads bundled resources.

Examples

Fonts

Images

Icons

Sounds

Read Only

--------------------------------------------------

data_path()

Loads runtime files.

Examples

Products

Bills

History

Configuration

Counters

Barcode PDFs

Invoice PDFs

Read Write

--------------------------------------------------

# 123. Runtime Data Folder

Application data is stored in

LocalAppData

QuickBill

Contains

products.json

config.json

bill_counter.json

held_bills.json

bills_history.json

bills/

barcodes/

Advantages

No Administrator Rights

Cleaner installation

Professional behaviour

Easy updates

--------------------------------------------------

# 124. First Launch

On first startup

QuickBill automatically creates

LocalAppData

↓

QuickBill

↓

Required folders

↓

Required JSON files

↓

Default configuration

User never needs to create files manually.

--------------------------------------------------

# 125. Folder Creation

Automatically created

bills/

barcodes/

Automatically created JSON

products.json

config.json

bill_counter.json

held_bills.json

bills_history.json

Application always checks existence before use.

--------------------------------------------------

# 126. Installer

Current installer

Inno Setup

Wizard Style

Modern

Compression

LZMA2

Solid Compression

Enabled

Produces

Professional Windows installer.

--------------------------------------------------

# 127. Installer Features

Current Features

Welcome Screen

License Agreement

Installation Folder

Desktop Shortcut

Start Menu Shortcut

Application Icon

Professional Wizard

Progress Bar

Finish Screen

Uninstaller

--------------------------------------------------

# 128. Installer Information

Current metadata

Application Name

Version

Publisher

Description

Copyright

Architecture

Output Filename

Application Directory

--------------------------------------------------

# 129. Installation Directory

Default

Program Files

QuickBill

Application files remain here.

User data does NOT.

--------------------------------------------------

# 130. User Data Directory

Default

LocalAppData

QuickBill

Advantages

User files survive application updates.

Professional Windows standard.

--------------------------------------------------

# 131. Uninstaller

Automatically generated by

Inno Setup.

Capabilities

Remove executable

Remove shortcuts

Remove Start Menu entries

Registered inside

Windows Apps & Features

Professional uninstall experience.

--------------------------------------------------

# 132. Installer Compression

Current

LZMA2

Solid Compression

Purpose

Reduce installer size.

Faster downloads.

Professional distribution.

--------------------------------------------------

# 133. Release Folder

Current structure

release/

Contains

Final Setup Executable

Ready for distribution.

Nothing else should be placed here.

--------------------------------------------------

# 134. Git Repository

Repository stores

Source Code

Assets

Specification Files

Installer Scripts

Documentation

Does NOT permanently store

Generated executable

Temporary build folders

User runtime data

--------------------------------------------------

# 135. Ignored Files

Git ignores

build/

dist/

__pycache__/

Local runtime files

Generated PDFs

Generated barcode sheets

Keeps repository clean.

--------------------------------------------------

# 136. Release Checklist

Before release

✓ Update version

✓ Test application

✓ Build executable

✓ Test executable

✓ Build installer

✓ Test installer

✓ Test uninstall

✓ Verify icons

✓ Verify version info

✓ Push source code

✓ Upload installer

--------------------------------------------------

# 137. Version Upgrade Procedure

Current workflow

Increase version number

↓

Update VERSIONINFO

↓

Update Installer Version

↓

Rebuild EXE

↓

Rebuild Installer

↓

Test

↓

Release

--------------------------------------------------

# 138. Testing Checklist

Application starts

Scanner works

Products load

Products save

Bills generate

PDF opens

Barcode PDF works

History works

Hold Bill works

Settings save

Installer installs

Uninstaller removes

Desktop shortcut works

Start Menu works

--------------------------------------------------

# 139. Known Design Decisions

JSON chosen instead of SQLite.

Reason

Simple

Portable

Readable

Offline

Easy backup

Tkinter selected because

Lightweight

Native

Fast

No web runtime required.

--------------------------------------------------

# 140. Future Release Goals

Version 2.x

Customer Module

Reports

Sales Dashboard

Dark Theme

Printer Integration

Version 3.x

SQLite Database

Authentication

Employee Accounts

Backup Manager

Cloud Sync

Analytics

GST Reports

Multi-terminal Support

--------------------------------------------------

# 141. Long-Term Vision

QuickBill is intended to evolve into a complete retail ERP.

Future modules may include

Customers

Suppliers

Purchase Orders

Expense Tracking

Sales Reports

Profit Analysis

Inventory Analytics

GST Reports

Thermal Printer Support

Receipt Designer

Barcode Scanner Configuration

Automatic Backup

Cloud Synchronization

Role-Based Access

License Activation

Plugin System

--------------------------------------------------

# 142. Development Principles

Every new feature should

Follow existing folder structure

Remain modular

Avoid duplicated code

Use helper functions

Separate UI and logic

Preserve backward compatibility

Maintain offline-first design

--------------------------------------------------

# 143. Project Status

Current Version

v2.0.0

Status

Production Ready

Application

Stable

Installer

Stable

Packaging

Stable

Runtime Storage

Stable

PDF Generation

Stable

Barcode System

Stable

Ready for future feature development.

--------------------------------------------------
