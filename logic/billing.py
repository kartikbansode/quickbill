from logic.cart import cart
from logic.config import get_tax_percent, get_discount_percent, get_round_off

def calculate_totals(items=None, tax_percent=None, discount_percent=None, round_off=None):
    source = cart if items is None else items
    
    if tax_percent is None:
        tax_percent = get_tax_percent()
    if discount_percent is None:
        discount_percent = get_discount_percent()
    if round_off is None:
        round_off = get_round_off()

    subtotal = sum(
        float(item.get("price", item.get("selling_price", 0))) * int(item.get("qty", 0))
        for item in source
    )
    tax = round(subtotal * (tax_percent / 100), 2)
    discount = round(subtotal * (discount_percent / 100), 2)
    total = subtotal + tax - discount
    
    if round_off:
        total = round(total)
    else:
        total = round(total, 2)
        
    return round(subtotal, 2), tax, discount, total
