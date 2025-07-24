# logic/database.py

# In-memory mock product database
product_data = {
    "927454336": ("927454336", "Coca Cola", 40),
    "732709537": ("732709537", "Pepsi", 35),
    "578953784": ("578953784", "Biscuits", 20),
    "467844357": ("467844357", "Chips", 25),
    # Add more barcodes as needed
}

def get_product_by_barcode(barcode):
    return product_data.get(barcode)

# Stubbed functions for compatibility (if app.py calls them)
def init_product_db():
    print("[INFO] Product DB initialized (in-memory)")

def init_bill_db():
    print("[INFO] Bill DB initialized (stub)")
