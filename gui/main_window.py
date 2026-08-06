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
from gui.dialogs.add_product_dialog import AddProductDialog
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

scanner_active = False
webcam_url = "http://192.168.0.133:8080/video"  # Default webcam URL
BILLS_HISTORY_FILE = "bills_history.json"


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
        window.iconbitmap("assets/images/logo.ico")  # Set icon
    except:
        print("Icon file not found, using default icon.")

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
            text="▶ Start Scanner",
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

        refresh_product_table()

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

    def on_barcode_detected(barcode):

        product = get_product_by_barcode(barcode)

        if product:

            add_to_cart(product)

            play_beep()

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

    # --- Settings View ---
    settings_frame = tk.Frame(content_container, bg="#e9ecef")

    # Back to Billing Button
    back_button_frame = tk.Frame(settings_frame, bg="#e9ecef")
    back_button_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Button(
        back_button_frame,
        text="← Back to Billing",
        font=("Helvetica", 10, "bold"),
        bg="#6c757d",
        fg="white",
        command=lambda: show_billing_view(),
    ).pack(side=tk.LEFT)

    # Webcam URL Section
    url_frame = tk.LabelFrame(
        settings_frame,
        text="Webcam URL",
        font=("Helvetica", 11, "bold"),
        bg="white",
        fg="#2c3e50",
    )
    url_frame.pack(padx=10, pady=5, fill=tk.X)

    tk.Label(url_frame, text="URL:", font=("Helvetica", 10), bg="white").pack(
        side=tk.LEFT, padx=5
    )
    url_entry = tk.Entry(url_frame, width=40, font=("Helvetica", 10))
    url_entry.insert(0, webcam_url)
    url_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def save_url():
        global webcam_url
        new_url = url_entry.get().strip()
        if new_url:
            webcam_url = new_url
            if scanner_active:
                stop_scanner()
                billing_view.update_scanner_status(
                    "📡 Scanner restarting with new URL..."
                )
                scan_barcode_background(webcam_url, on_barcode_detected)
            messagebox.showinfo("Success", "Webcam URL updated successfully.")
        else:
            messagebox.showwarning("Invalid URL", "Please enter a valid webcam URL.")

    tk.Button(
        url_frame,
        text="Save",
        font=("Helvetica", 10, "bold"),
        bg="#28a745",
        fg="white",
        command=save_url,
    ).pack(side=tk.LEFT, padx=5)

    def edit_selected_product():

        selected = product_tree.selection()

        if not selected:

            messagebox.showwarning("Edit Product", "Please select a product.")

            return

        values = product_tree.item(selected[0])["values"]

        barcode = str(values[0])

        product = get_product_by_barcode(barcode)

        if not product:

            messagebox.showerror("Error", "Product not found.")

            return

        AddProductDialog(
            product_frame, refresh_callback=refresh_product_table, product=product
        )

    def open_add_product_window():

        AddProductDialog(product_frame, refresh_callback=refresh_product_table)

    def delete_selected_product():

        selected = product_tree.selection()

        if not selected:

            messagebox.showwarning("Delete Product", "Please select a product.")

            return

        values = product_tree.item(selected[0])["values"]

        barcode = str(values[0])

        name = values[2]

        if not messagebox.askyesno("Delete Product", f"Delete '{name}' ?"):
            return

        ok, msg = delete_product(barcode)

        if ok:

            refresh_product_table()

            messagebox.showinfo("Success", "Product deleted successfully.")

        else:

            messagebox.showerror("Error", msg)

    # ==========================================================
    # PRODUCT TABLE
    # ==========================================================

    product_frame = tk.LabelFrame(
        settings_frame,
        text="Product Master",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        fg="#2c3e50",
    )
    product_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(8, 10))

    # ==========================================================
    # PRODUCT TOOLBAR
    # ==========================================================

    toolbar = tk.Frame(product_frame, bg="white")
    toolbar.pack(fill=tk.X, padx=5, pady=5)

    tk.Button(
        toolbar,
        text="+ Add Product",
        bg="#28a745",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=15,
        command=lambda: open_add_product_window(),
    ).pack(side=tk.LEFT)

    tk.Button(
        toolbar,
        text="Edit",
        width=10,
        command=edit_selected_product,
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        toolbar,
        text="Delete",
        width=10,
        command=delete_selected_product,
    ).pack(side=tk.LEFT)

    # =========================
    # Search Bar
    # =========================

    search_frame = tk.Frame(product_frame, bg="white")
    search_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

    tk.Label(
        search_frame,
        text="Search :",
        bg="white",
        font=("Segoe UI", 10, "bold"),
    ).pack(side=tk.LEFT)

    search_var = tk.StringVar()

    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        width=35,
        font=("Segoe UI", 10),
    )

    search_entry.pack(side=tk.LEFT, padx=8)

    product_count = tk.StringVar(value="Total Products : 0")

    tk.Label(
        search_frame,
        textvariable=product_count,
        bg="white",
        fg="gray",
        font=("Segoe UI", 9, "bold"),
    ).pack(side=tk.RIGHT)

    search_var.trace_add("write", lambda *args: refresh_product_table())

    product_columns = (
        "Barcode",
        "SKU",
        "Product Name",
        "Brand",
        "Category",
        "Stock",
        "Price",
        "GST",
    )

    product_tree = ttk.Treeview(
        product_frame, columns=product_columns, show="headings", height=18
    )

    column_widths = {
        "Barcode": 100,
        "SKU": 70,
        "Product Name": 180,
        "Brand": 90,
        "Category": 90,
        "Stock": 60,
        "Price": 70,
        "GST": 50,
    }

    for col in product_columns:
        product_tree.heading(col, text=col)
        product_tree.column(col, width=column_widths[col], anchor="center")

    product_tree.column("Product Name", anchor="w")

    scroll_y = ttk.Scrollbar(
        product_frame, orient="vertical", command=product_tree.yview
    )

    scroll_x = ttk.Scrollbar(
        product_frame, orient="horizontal", command=product_tree.xview
    )

    product_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    product_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 0))

    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(fill=tk.X)

    def refresh_product_table():

        product_tree.delete(*product_tree.get_children())

        keyword = search_var.get().strip()

        if keyword:

            products = search_products(keyword)

        else:

            products = get_all_products()

        # <-- ADD THESE TWO LINES HERE
        product_count.set(f"Total Products : {len(products)}")

        for product in products:

            product_tree.insert(
                "",
                tk.END,
                values=(
                    product.get("barcode", ""),
                    product.get("sku", ""),
                    product.get("name", ""),
                    product.get("brand", ""),
                    product.get("category", ""),
                    product.get("stock", 0),
                    f"₹ {float(product.get('selling_price',0)):.2f}",
                    f"{product.get('gst',0)} %",
                ),
            )

    product_tree.bind("<Double-1>", lambda event: edit_selected_product())

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

    toolbar = Toolbar(
        window,
        {
            "new_bill": clear_cart_all,
            "save_bill": lambda: None,
            "print_bill": lambda: None,
            "hold_bill": hold_current_bill,
            "find_bill": lambda: show_find_bill_view(),
            "products": lambda: show_settings_view(),
            "settings": lambda: show_settings_view(),
            "customers": lambda: None,
            "reports": lambda: None,
            "exit": window.destroy,
        },
    )

    toolbar.pack(fill="x")

    # =====================================================
    # View Switching Functions
    # =====================================================

    def show_billing_view():

        settings_frame.pack_forget()

        find_bill_view.pack_forget()

        billing_view.pack(fill="both", expand=True)

        window.title("QuickBill System - Billing")

        if scanner_active:

            billing_view.update_scanner_status("Scanner Active")

        else:

            billing_view.update_scanner_status("Ready")

    def show_settings_view():

        global scanner_active

        refresh_product_table()

        billing_view.pack_forget()

        find_bill_view.pack_forget()

        settings_frame.pack(fill="both", expand=True)

        window.title("QuickBill System - Products")

        if scanner_active:

            stop_scanner()

            scanner_active = False

    def show_find_bill_view():

        global scanner_active

        billing_view.pack_forget()

        settings_frame.pack_forget()

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
        },
    )

    # =====================================================
    # Initialize
    # =====================================================

    show_billing_view()

    window.mainloop()
