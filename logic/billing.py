# logic/billing.py

from logic.cart import cart  # ✅ IMPORT shared cart

def calculate_totals():
    subtotal = 0.0
    for item in cart:
        subtotal += item['price'] * item['qty']
    tax = subtotal * 0.18  # Example: 18% GST
    discount = 0.0         # You can apply logic later
    total = subtotal + tax - discount
    return subtotal, tax, discount, total
