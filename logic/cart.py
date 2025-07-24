cart = []

def add_to_cart(name, price):
    for item in cart:
        if item['name'] == name:
            item['qty'] += 1
            item['total'] = item['qty'] * item['price']
            return
    cart.append({'name': name, 'price': price, 'qty': 1, 'total': price})

def remove_from_cart(index):
    if 0 <= index < len(cart):
        del cart[index]

def calculate_totals():
    subtotal = sum(item['total'] for item in cart)
    tax = subtotal * 0.18  # 18% tax
    discount = subtotal * 0.05  # 5% discount
    total = subtotal + tax - discount
    return subtotal, tax, discount, total

def clear_cart():
    cart.clear()
