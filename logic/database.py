# logic/database.py
import sqlite3
import os

DATA_FOLDER = "data"
PRODUCT_DB = os.path.join(DATA_FOLDER, "products.db")
BILL_DB = os.path.join(DATA_FOLDER, "bills.db")

def init_product_db():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    conn = sqlite3.connect(PRODUCT_DB)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            barcode TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            unique_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

def init_bill_db():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    conn = sqlite3.connect(BILL_DB)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            customer_name TEXT,
            customer_phone TEXT,
            total REAL,
            items TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_product_by_barcode(barcode):
    conn = sqlite3.connect(PRODUCT_DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE barcode = ?", (barcode,))
    row = cur.fetchone()
    conn.close()
    return row

import csv
import os

PRODUCTS_FILE = os.path.join("data", "products.csv")

def get_product_by_barcode(barcode):
    try:
        with open(PRODUCTS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["barcode"] == barcode:
                    return row["barcode"], row["name"], float(row["price"])
    except FileNotFoundError:
        print(f"⚠️ File not found: {PRODUCTS_FILE}")
    return None
