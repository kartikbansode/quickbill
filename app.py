# app.py
from logic.database import init_product_db, init_bill_db
from gui.main_window import launch_main_window

def main():
    print("Initializing Billing System...")
    init_product_db()
    init_bill_db()
    launch_main_window()

if __name__ == "__main__":
    main()
