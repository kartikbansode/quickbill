import time

from logic.customer_display_server import customer_display


print("Starting QuickBill Customer Display Payment Test...")

customer_display.start()

time.sleep(1)

print("Server started.")
print("Waiting for Android connection...")
print("Press Ctrl+C to stop.")

try:

    while True:

        command = input(
            "\nEnter event "
            "(start/pending/completed/cancel/sale/new/quit): "
        ).strip().lower()

        if command == "start":

            customer_display.payment_started(
                "QB-TEST-0001",
                "UPI",
                250.00,
            )

            print("payment_started sent.")

        elif command == "pending":

            customer_display.payment_pending(
                "QB-TEST-0001",
                "UPI",
                250.00,
            )

            print("payment_pending sent.")

        elif command == "completed":

            customer_display.payment_completed(
                "QB-TEST-0001",
                "UPI",
                250.00,
            )

            print("payment_completed sent.")

        elif command == "cancel":

            customer_display.payment_cancelled(
                "QB-TEST-0001",
                "UPI",
            )

            print("payment_cancelled sent.")

        elif command == "sale":

            customer_display.sale_completed(
                "QB-TEST-0001",
                "UPI",
                250.00,
            )

            print("sale_completed sent.")

        elif command == "new":

            customer_display.new_bill(
                "QB-TEST-0002"
            )

            print("new_bill sent.")

        elif command == "quit":

            break

        else:

            print(
                "Use: "
                "start, pending, completed, "
                "cancel, sale, new, quit"
            )

finally:

    print("\nStopping server...")

    customer_display.stop()

    print("Server stopped.")