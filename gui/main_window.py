import tkinter as tk
from tkinter import ttk, messagebox
from logic.cart import cart, add_to_cart, remove_from_cart, update_quantity
from logic.billing import calculate_totals
from logic.barcode_scanner import scan_barcode_background, stop_scanner, play_beep
from logic.database import (
    get_product_by_barcode,
    add_product,
    edit_product,
    delete_product,
    get_all_products,
    search_products,
)
from logic.pdf_generator import generate_pdf_bill
import os
import json
from gui.toolbar import Toolbar
from gui.header import Header
from gui.statusbar import StatusBar
from gui.billing.billing_view import BillingView
from gui.product_master import ProductMaster
from gui.settings_view import SettingsView
from gui.payment.payment_dialog import PaymentDialog
from logic.hold_bill import hold_bill
from gui.hold_bill.hold_bill_window import HoldBillWindow
from gui.find_bill.find_bill_view import FindBillView
from logic.bill_history import (
    get_all_bills,
    search_bill_history,
)
from logic.database import generate_bill_number
from gui.find_bill.bill_details_dialog import BillDetailsDialog
from logic.resource_path import resource_path
from logic.file_paths import app_path

scanner_active = False
webcam_url = "http://192.168.0.203:8080/video"  # Default webcam URL


BILLS_HISTORY_FILE = app_path("bills_history.json")


def launch_main_window():

    window = tk.Tk()

    window.attributes("-fullscreen", True)

    window.title("QuickBill System")

    window.bind(
        "<Escape>",
        lambda e: window.attributes("-fullscreen", False),
    )

    find_bill_view = None
    try:
        logo = tk.PhotoImage(file=resource_path("assets/images/logo.png"))
        window.iconphoto(True, logo)
    except Exception as e:
        print("Unable to load icon:", e)

    # Set window size and center it
    window_width = 1000
    window_height = 650
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.configure(bg="#e9ecef")
    window.resizable(True, True)  # Enable resizing and maximize button

    # Custom style for professional look
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TButton",
        font=("Helvetica", 10, "bold"),
        padding=8,
        background="#007bff",
        foreground="white",
    )
    style.map("TButton", background=[("active", "#0056b3")])
    style.configure(
        "TLabelFrame",
        font=("Helvetica", 11, "bold"),
        foreground="#2c3e50",
        background="white",
    )
    style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
    style.configure(
        "Treeview.Heading",
        font=("Helvetica", 10, "bold"),
        background="#007bff",
        foreground="white",
    )
    style.configure("Bold.Treeview", font=("Helvetica", 9, "bold"))

    # --- Menu Bar ---
    header = Header(window)
    header.pack(fill="x")

    status_bar = StatusBar(window)
    status_bar.pack(fill="x")

    # --- Content Container ---
    content_container = tk.Frame(window, bg="#e9ecef")
    content_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # --- Billing View ---
    billing_view = None

    def refresh_table():
        if billing_view is None:
            return
        billing_view.render_cart(cart)
        billing_view.refresh_totals()

    def update_totals():
        if billing_view is not None:
            billing_view.refresh_totals()

    def add_manual_barcode():
        if billing_view is None:
            return

        barcode = billing_view.get_manual_barcode()

        if barcode:

            on_barcode_detected(barcode)

            billing_view.clear_manual_barcode()

            billing_view.focus_manual_barcode()

    def clear_cart_all():
        if messagebox.askyesno(
            "Clear All", "Are you sure you want to clear the entire cart?"
        ):
            cart.clear()
            refresh_table()

    def update_item_qty(index, delta):
        current = cart[index]["qty"]
        new_qty = current + delta
        if new_qty < 1:
            remove_from_cart(index)
        else:
            update_quantity(index, new_qty)
        refresh_table()

    def increase_item_qty(index):
        update_item_qty(index, 1)

    def decrease_item_qty(index):
        update_item_qty(index, -1)

    def delete_item(index):
        remove_from_cart(index)
        refresh_table()

    def start_scan():
        global scanner_active
        if not scanner_active:
            scanner_active = True
            billing_view.update_scanner_status("Scanner Active")
            status_bar.scanner_connected()
            status_bar.set_status("Scanning Product")
            scan_barcode_background(webcam_url, on_barcode_detected)

    def stop_scan():
        global scanner_active
        if scanner_active:
            stop_scanner()
            scanner_active = False

    try:
        billing_view.scanner_panel.scan_button.config(
            text="Start Scanner",
            bg="#28a745",
        )
    except:
        pass

    def open_payment_dialog():

        if not cart:
            messagebox.showwarning("Empty Bill", "Please add at least one product.")
            return

        subtotal, tax, discount, total = calculate_totals()

        PaymentDialog(
            window,
            total,
            complete_sale,
        )

    def complete_sale(payment_mode, received_amount):

        nonlocal bill_number

        completed_bill = bill_number

        # --------------------------------
        # Generate PDF & Save Bill
        # --------------------------------

        generate_pdf_bill(
            cart,
            completed_bill,
            payment_mode,
            received_amount,
        )

        # --------------------------------
        # Reduce Product Stock
        # --------------------------------

        for item in cart:

            product = get_product_by_barcode(item["barcode"])

            if product:

                product["stock"] -= item["qty"]

                edit_product(product["barcode"], product)

        # --------------------------------
        # Refresh Product Table
        # --------------------------------

        product_view.refresh_table()

        # --------------------------------
        # Clear Current Cart
        # --------------------------------

        cart.clear()

        refresh_table()

        # --------------------------------
        # Success Message
        # --------------------------------

        messagebox.showinfo(
            "Sale Completed", f"Invoice {completed_bill} generated successfully."
        )

        # --------------------------------
        # Generate Next Bill Number
        # --------------------------------

        bill_number = generate_bill_number()

        billing_view.set_bill_number(bill_number)

        status_bar.set_bill_number(bill_number)

    def search_bill(keyword):

        find_bill_view.clear_table()

        bills = search_bill_history(keyword)

        bills.reverse()

        for bill in bills:

            find_bill_view.add_bill(
                bill["bill_no"],
                bill["date"],
                bill.get("payment_mode", "-"),
                len(bill["items"]),
                f"₹ {bill['total']:.2f}",
            )

    def open_bill_details(bill_no):

        bills = get_all_bills()

        for bill in bills:

            if bill["bill_no"] == bill_no:

                BillDetailsDialog(
                    window,
                    bill,
                )

                return

    def reprint_bill(bill_no):

        bills = get_all_bills()

        for bill in bills:

            if bill["bill_no"] == bill_no:

                generate_pdf_bill(
                    bill["items"],
                    bill["bill_no"],
                    bill.get("payment_mode", "Cash"),
                    bill.get("received_amount", bill["total"]),
                )

                messagebox.showinfo(
                    "Reprint", f"Invoice {bill_no} has been regenerated."
                )

                return

        messagebox.showerror("Error", "Bill not found.")

    def delete_bill(bill_no):

        if not messagebox.askyesno(
            "Delete Bill", f"Are you sure you want to delete\n{bill_no}?"
        ):
            return

        try:

            with open(BILLS_HISTORY_FILE, "r", encoding="utf-8") as file:
                bills = json.load(file)

            new_bills = [bill for bill in bills if bill["bill_no"] != bill_no]

            with open(BILLS_HISTORY_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    new_bills,
                    file,
                    indent=4,
                )

            load_bill_history()

            messagebox.showinfo("Success", "Bill deleted successfully.")

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e),
            )

    def on_barcode_detected(barcode):

        product = get_product_by_barcode(barcode)

        if product:

            add_to_cart(product)

            refresh_table()

            billing_view.display_product(product)

            billing_view.update_scanner_status("Product Added")

            status_bar.scanner_connected()

            status_bar.set_status(f"Added : {product['name']}")

        else:

            billing_view.update_scanner_status("Barcode Not Found")

            status_bar.set_status("Barcode Not Found")

    def hold_current_bill():

        nonlocal bill_number

        # -----------------------------------
        # Resume Existing Hold
        # -----------------------------------

        if not cart:

            HoldBillWindow(
                window,
                resume_hold_bill,
            )

            return

        # -----------------------------------
        # Hold Current Cart
        # -----------------------------------

        hold_no = hold_bill(cart.copy())

        messagebox.showinfo("Hold Bill", f"Current bill saved.\n\n{hold_no}")

        cart.clear()

        refresh_table()

    def resume_hold_bill(bill):

        nonlocal bill_number

        cart.clear()

        cart.extend(bill["cart"])

        refresh_table()

        bill_number = generate_bill_number()

        billing_view.set_bill_number(bill_number)

        status_bar.set_bill_number(bill_number)

        messagebox.showinfo("Hold Bill", f"{bill['hold_no']} resumed successfully.")

    billing_view = BillingView(
        content_container,
        {
            "generate_bill": open_payment_dialog,
            "clear_cart": clear_cart_all,
            "hold_bill": lambda: None,
            "start_scan": start_scan,
            "stop_scan": stop_scan,
            "barcode": on_barcode_detected,
            "increase_qty": increase_item_qty,
            "decrease_qty": decrease_item_qty,
            "delete_item": delete_item,
            "calculate_totals": calculate_totals,
        },
    )

    bill_number = generate_bill_number()
    status_bar.set_bill_number(bill_number)

    billing_view.set_bill_number(bill_number)

    billing_view.pack(fill="both", expand=True)

    # =====================================================
    # Product Master
    # =====================================================

    product_view = ProductMaster(content_container)

    # =====================================================
    # Settings
    # =====================================================

    def save_webcam_url(url):
        global webcam_url

        webcam_url = url

        if scanner_active:
            stop_scanner()

    settings_view = SettingsView(
        content_container,
        webcam_url=webcam_url,
        save_callback=save_webcam_url,
    )

    # =====================================================
    # Find Bill Functions
    # =====================================================

    def start_bill_scan():

        global scanner_active

        if not scanner_active:

            scanner_active = True

            status_bar.scanner_connected()

            status_bar.set_status("Scanning Bill")

            scan_barcode_background(
                webcam_url,
                on_bill_barcode_detected,
            )

    def stop_bill_scan():

        global scanner_active

        if scanner_active:

            stop_scanner()

            scanner_active = False

            status_bar.scanner_disconnected()

            status_bar.set_status("Ready")

    def on_bill_barcode_detected(barcode):

        global scanner_active

        find_bill_view.bill_search_var.set(barcode)

        search_bill(barcode)

        stop_bill_scan()

    def load_bill_history():

        find_bill_view.clear_table()

        bills = get_all_bills()

        bills.reverse()

        for bill in bills:

            find_bill_view.add_bill(
                bill["bill_no"],
                bill["date"],
                bill.get("payment_mode", "-"),
                len(bill["items"]),
                f"₹ {bill['total']:.2f}",
            )

    def search_bill(keyword):

        find_bill_view.clear_table()

        bills = search_bill_history(keyword)

        bills.reverse()

        for bill in bills:

            find_bill_view.add_bill(
                bill["bill_no"],
                bill["date"],
                bill.get("payment_mode", "-"),
                len(bill["items"]),
                f"₹ {bill['total']:.2f}",
            )

    # =====================================================
    # View Switching Functions
    # =====================================================

    def show_billing_view():

        product_view.pack_forget()

        settings_view.pack_forget()

        find_bill_view.pack_forget()

        billing_view.pack(fill="both", expand=True)

        window.title("QuickBill System - Billing")

        if scanner_active:

            billing_view.update_scanner_status("Scanner Active")

        else:

            billing_view.update_scanner_status("Ready")

    def show_products_view():

        global scanner_active

        billing_view.pack_forget()

        settings_view.pack_forget()

        find_bill_view.pack_forget()

        product_view.refresh_table()

        product_view.pack(fill="both", expand=True)

        window.title("QuickBill System - Product Master")

        if scanner_active:

            stop_scanner()

            scanner_active = False

    def show_settings_view():

        global scanner_active

        billing_view.pack_forget()

        product_view.pack_forget()

        find_bill_view.pack_forget()

        settings_view.pack(fill="both", expand=True)

        window.title("QuickBill System - Settings")

        if scanner_active:

            stop_scanner()

            scanner_active = False

    def show_find_bill_view():

        global scanner_active

        billing_view.pack_forget()

        product_view.pack_forget()

        settings_view.pack_forget()

        find_bill_view.bill_search_var.set("")

        load_bill_history()

        find_bill_view.pack(fill="both", expand=True)

        window.title("QuickBill System - Find Bill")

        if scanner_active:

            stop_scanner()

            scanner_active = False

    find_bill_view = FindBillView(
        content_container,
        {
            "back": show_billing_view,
            "search": search_bill,
            "refresh": load_bill_history,
            "view": open_bill_details,
            "reprint": reprint_bill,
            "delete": delete_bill,
        },
    )

    toolbar = Toolbar(
        window,
        {
            "billing": show_billing_view,
            "new_bill": clear_cart_all,
            "save_bill": lambda: None,
            "print_bill": lambda: None,
            "hold_bill": hold_current_bill,
            "find_bill": lambda: show_find_bill_view(),
            "products": show_products_view,
            "settings": show_settings_view,
            "customers": lambda: None,
            "reports": lambda: None,
            "exit": window.destroy,
        },
    )

    toolbar.pack(fill="x")

    # =====================================================
    # Initialize
    # =====================================================

    show_billing_view()

    window.mainloop()
