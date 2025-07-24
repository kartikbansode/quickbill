# logic/cart.py

cart = []

def add_to_cart(name, price):
    for item in cart:
        if item['name'] == name:
            item['qty'] += 1
            item['total'] = item['price'] * item['qty']
            return
    cart.append({'name': name, 'price': price, 'qty': 1, 'total': price})

def remove_from_cart(index):
    if 0 <= index < len(cart):
        del cart[index]

def update_quantity(index, qty):
    if 0 <= index < len(cart):
        cart[index]['qty'] = qty
        cart[index]['total'] = cart[index]['price'] * qty
