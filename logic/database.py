# logic/database.py

# In-memory mock product database
product_data = {
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

def get_product_by_barcode(barcode):
    return product_data.get(barcode)

# Stubbed functions for compatibility (if app.py calls them)
def init_product_db():
    print("[INFO] Product DB initialized (in-memory)")

def init_bill_db():
    print("[INFO] Bill DB initialized (stub)")