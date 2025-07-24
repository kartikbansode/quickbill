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
        cart.pop(index)

def update_quantity(index, new_qty):
    if 0 <= index < len(cart):
        cart[index]['qty'] = new_qty
        cart[index]['total'] = new_qty * cart[index]['price']
