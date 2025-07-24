from logic.cart import cart

def calculate_totals():
    subtotal = sum(item['price'] * item['qty'] for item in cart)
    tax = round(subtotal * 0.10, 2)  # 10% tax
    discount = round(subtotal * 0.05, 2)  # 5% discount
    total = subtotal + tax - discount
    return subtotal, tax, discount, total
