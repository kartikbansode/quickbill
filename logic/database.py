# logic/database.py
import json
import os
from logic.file_paths import app_path

# Initial product data (used if products.json doesn't exist)
initial_product_data = {
    "5923746501": {
        "barcode": "5923746501",
        "sku": "SKU001",
        "name": "Lay's Classic Salted Chips (52g)",
        "brand": "Lay's",
        "category": "Snacks",
        "purchase_price": 15,
        "selling_price": 20,
        "mrp": 20,
        "gst": 12,
        "stock": 100,
        "min_stock": 10,
        "supplier": "Default Supplier",
        "unit": "Packet",
        "weight": "52 g",
        "expiry": "",
        "batch": "",
        "hsn": "",
        "description": "",
    }
}

# Global product data (loaded from file or initialized)
product_data = {}

BILL_COUNTER_FILE = app_path("bill_counter.json")
PRODUCTS_FILE = app_path("products.json")


def load_products():
    global product_data

    if not os.path.exists(PRODUCTS_FILE):

        product_data = initial_product_data.copy()

        save_products()

        return

    try:

        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:

            product_data = json.load(f)

            product_data = {str(k): v for k, v in product_data.items()}

    except (json.JSONDecodeError, OSError):

        product_data = initial_product_data.copy()

        save_products()


def save_products():
    try:
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump(product_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Failed to save products: {e}")


def get_product_by_barcode(barcode):
    return product_data.get(str(barcode), None)


def add_product(barcode, product):
    """Add a new product to the database."""

    barcode = str(barcode)

    if barcode in product_data:
        return False, "Barcode already exists."

    try:

        selling_price = float(product.get("selling_price", 0))

        if selling_price < 0:
            return False, "Selling price cannot be negative."

        product_data[barcode] = product

        save_products()

        return True, "Product added successfully."

    except Exception as e:

        return False, str(e)


def edit_product(barcode, product):
    """Update an existing product."""

    barcode = str(barcode)

    if barcode not in product_data:
        return False, "Barcode not found."

    try:

        selling_price = float(product.get("selling_price", 0))

        if selling_price < 0:
            return False, "Selling price cannot be negative."

        product_data[barcode] = product

        save_products()

        return True, "Product updated successfully."

    except Exception as e:

        return False, str(e)


def delete_product(barcode):
    """Delete a product from the database and save to file."""
    barcode = str(barcode)
    print(f"[DEBUG] Attempting to delete barcode: {barcode}")
    if barcode not in product_data:
        print(
            f"[DEBUG] Barcode {barcode} not found in product_data: {list(product_data.keys())}"
        )
        return False, f"Barcode {barcode} not found."
    del product_data[barcode]
    save_products()
    print(f"[DEBUG] Barcode {barcode} deleted successfully.")
    return True, "Product deleted successfully."


def get_all_products():
    """Return all products in the database."""
    return list(product_data.values())


# Stubbed functions for compatibility
def init_product_db():
    print("[INFO] Product DB initialized (in-memory)")
    load_products()


def init_bill_db():
    print("[INFO] Bill DB initialized (stub)")


def search_products(keyword):

    keyword = keyword.lower().strip()

    if not keyword:
        return []

    results = []

    for product in product_data.values():

        if (
            keyword in product["name"].lower()
            or keyword in product["barcode"].lower()
            or keyword in product["brand"].lower()
            or keyword in product["category"].lower()
        ):

            results.append(product)

    return results


import datetime


def generate_bill_number():
    """
    Generates bill numbers like:
    QB-20260805-000001
    """

    today = datetime.datetime.now().strftime("%Y%m%d")

    data = {
        "date": today,
        "counter": 0,
    }

    if os.path.exists(BILL_COUNTER_FILE):

        try:

            with open(BILL_COUNTER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        except Exception:
            pass

    if data["date"] != today:

        data["date"] = today
        data["counter"] = 1

    else:

        data["counter"] += 1

    with open(BILL_COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )

    return f"QB-{today}-{data['counter']:06d}"
