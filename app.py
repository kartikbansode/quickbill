from gui.splash_screen import SplashScreen
from logic.database import init_product_db, init_bill_db
from logic.customer_display_server import customer_display
from gui.main_window import launch_main_window

import time


def main():

    splash = SplashScreen()

    splash.update(10, "Initializing QuickBill...")
    time.sleep(0.3)

    splash.update(30, "Loading Product Database...")
    init_product_db()
    time.sleep(0.3)

    splash.update(55, "Loading Billing History...")
    init_bill_db()
    time.sleep(0.3)

    splash.update(75, "Preparing Workspace...")
    time.sleep(0.3)

    splash.update(90, "Initializing Barcode Scanner...")
    time.sleep(0.3)

    splash.update(95, "Starting Customer Display...")

    customer_display.start()

    time.sleep(0.3)

    splash.update(100, "Launching QuickBill...")

    time.sleep(0.2)

    splash.close()

    launch_main_window()


if __name__ == "__main__":
    main()
