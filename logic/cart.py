cart = []


def _get_item_rate(product):
    return product.get("selling_price", product.get("price", 0))


def add_to_cart(product):

    barcode = product["barcode"]

    for item in cart:

        if str(item["barcode"]) == str(barcode):

            item["qty"] += 1
            rate = _get_item_rate(item)
            item["price"] = rate
            item["selling_price"] = rate
            item["total"] = round(item["qty"] * rate, 2)
            return

    rate = _get_item_rate(product)

    cart.append({

        "barcode": product["barcode"],

        "sku": product["sku"],

        "name": product["name"],

        "brand": product["brand"],

        "category": product["category"],

        "purchase_price": product["purchase_price"],

        "price": rate,

        "selling_price": rate,

        "mrp": product["mrp"],

        "gst": product["gst"],

        "stock": product["stock"],

        "supplier": product["supplier"],

        "unit": product["unit"],

        "weight": product["weight"],

        "qty": 1,

        "total": rate

    })


def remove_from_cart(index):

    if 0 <= index < len(cart):

        cart.pop(index)


def update_quantity(index, qty):

    if 0 <= index < len(cart):
        
        qty = max(1, qty)

        cart[index]["qty"] = qty

        rate = _get_item_rate(cart[index])
        cart[index]["price"] = rate
        cart[index]["selling_price"] = rate
        cart[index]["total"] = round(qty * rate, 2)