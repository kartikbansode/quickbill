# logic/database.py
import json
import os

# Initial product data (used if products.json doesn't exist)
initial_product_data = {
    "5923746501": ("5923746501", "Lay's Classic Salted Chips (52g)", 20),
    "3849201756": ("3849201756", "Kurkure Masala Munch (55g)", 20),
    "7051938462": ("7051938462", "Bingo Mad Angles (50g)", 35),
    "2183094756": ("2183094756", "Doritos Nacho Cheese (70g)", 45),
    "6730291845": ("6730291845", "Haldiram’s Aloo Bhujia (200g)", 99),
    "4803921673": ("4803921673", "Pringles Sour Cream & Onion (107g)", 80),
    "9302857164": ("9302857164", "Peri Peri Makhana (roasted fox nuts) (60g)", 80),
    "5618203947": ("5618203947", "Cheese Balls (small pack)", 30),
    "7821304956": ("7821304956", "Popcorn (Act II / Ready-to-eat) (60g)", 100),
    "3194728560": ("3194728560", "Nachos with salsa dip (combo)", 25),
    "4029837156": ("4029837156", "Hide & Seek Fab (120g)", 25),
    "6571839204": ("6571839204", "Milkybar (small pack)", 10),
    "8901742635": ("8901742635", "Kinder Joy (20g)", 40)
}

# Global product data (loaded from file or initialized)
product_data = {}

# Path to the JSON file for persistent storage
PRODUCTS_FILE = "products.json"

def load_products():
    """Load products from products.json or use initial data if file doesn't exist."""
    global product_data
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r') as f:
                product_data = json.load(f)
                # Convert price to float and ensure tuple format
                product_data = {str(k): (str(k), v[1], float(v[2])) for k, v in product_data.items()}
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[ERROR] Corrupted products.json: {e}, using initial data.")
            product_data = initial_product_data.copy()
    else:
        product_data = initial_product_data.copy()
    save_products()  # Ensure file is created/updated

def save_products():
    """Save current product_data to products.json."""
    try:
        with open(PRODUCTS_FILE, 'w') as f:
            # Convert tuples to lists for JSON serialization
            json_data = {k: [v[0], v[1], v[2]] for k, v in product_data.items()}
            json.dump(json_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to save products: {e}")

def get_product_by_barcode(barcode):
    return product_data.get(str(barcode))

def add_product(barcode, name, price):
    """Add a new product to the database and save to file."""
    barcode = str(barcode)
    if barcode in product_data:
        return False, "Barcode already exists."
    try:
        price = float(price)
        if price < 0:
            return False, "Price cannot be negative."
        product_data[barcode] = (barcode, name, price)
        save_products()
        return True, "Product added successfully."
    except ValueError:
        return False, "Invalid price format."

def edit_product(barcode, name, price):
    """Edit an existing product in the database and save to file."""
    barcode = str(barcode)
    if barcode not in product_data:
        return False, "Barcode not found."
    try:
        price = float(price)
        if price < 0:
            return False, "Price cannot be negative."
        product_data[barcode] = (barcode, name, price)
        save_products()
        return True, "Product updated successfully."
    except ValueError:
        return False, "Invalid price format."

def delete_product(barcode):
    """Delete a product from the database and save to file."""
    barcode = str(barcode)
    print(f"[DEBUG] Attempting to delete barcode: {barcode}")
    if barcode not in product_data:
        print(f"[DEBUG] Barcode {barcode} not found in product_data: {list(product_data.keys())}")
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