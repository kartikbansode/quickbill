import time

from logic.customer_display_server import customer_display


def main():

    print("Starting customer display server...")

    customer_display.start()

    time.sleep(1)

    print("Server ready.")
    print("Waiting for test client...")

    time.sleep(5)

    bill = {
        "type": "bill_update",
        "bill_no": "QB-000001",
        "cashier": "Admin",

        "items": [
            {
                "name": "Parle-G",
                "qty": 2,
                "rate": 10.00,
                "amount": 20.00,
            },
            {
                "name": "Milk",
                "qty": 1,
                "rate": 32.00,
                "amount": 32.00,
            },
        ],

        "subtotal": 52.00,
        "tax": 5.20,
        "discount": 2.60,
        "total": 54.60,
    }

    print()
    print("Sending bill to customer display...")

    customer_display.broadcast(bill)

    print("Bill broadcast requested.")

    time.sleep(5)

    print()
    print("Stopping server...")

    customer_display.stop()

    print("Server stopped.")


if __name__ == "__main__":
    main()