# logic/billing.py

cart = []  # Global cart

def add_to_cart(item_name, price):
    for i in range(len(cart)):
        if cart[i]['name'] == item_name:
            cart[i]['qty'] += 1
            cart[i]['total'] = cart[i]['qty'] * cart[i]['price']
            return
    cart.append({
        'name': item_name,
        'qty': 1,
        'price': price,
        'total': price
    })

def remove_from_cart(item_name):
    global cart
    cart = [item for item in cart if item['name'] != item_name]

def update_qty(item_name, new_qty):
    for item in cart:
        if item['name'] == item_name:
            item['qty'] = new_qty
            item['total'] = new_qty * item['price']
            break

def calculate_totals(tax_percent=18, discount=0):
    subtotal = sum(item['total'] for item in cart)
    tax = subtotal * (tax_percent / 100)
    total = subtotal + tax - discount
    return subtotal, tax, discount, total  # ✅ Return correct variables
