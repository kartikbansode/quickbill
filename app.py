from logic.database import init_product_db, init_bill_db
from gui.main_window import launch_main_window
import os
import sys

def main():
    print("Running quickBill...")
    init_product_db()
    init_bill_db()
    launch_main_window()
    
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
    
if __name__ == "__main__":
    main()

