from logic.cart import cart

def calculate_totals(items=None, tax_percent=10, discount_percent=5):
    source = cart if items is None else items
    subtotal = sum(
        float(item.get("price", item.get("selling_price", 0))) * int(item.get("qty", 0))
        for item in source
    )
    tax = round(subtotal * (tax_percent / 100), 2)
    discount = round(subtotal * (discount_percent / 100), 2)
    total = round(subtotal + tax - discount, 2)
    return round(subtotal, 2), tax, discount, total
