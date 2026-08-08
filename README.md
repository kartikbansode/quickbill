# QuickBill

> **Latest Version:** 2.1.0  
> **Release Date:** August 2026

QuickBill is a modern desktop billing and inventory management application built with Python. It is designed for retail shops and small businesses, providing fast billing, barcode scanning, inventory management, barcode label generation, and professional PDF invoice creation through a simple and user-friendly interface.

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

Install dependencies:

```bash
pip install -r requirements.txt
```

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
