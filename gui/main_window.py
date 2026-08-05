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
from logic.database import edit_product
from logic.database import delete_product

scanner_active = False
webcam_url = "http://192.168.0.133:8080/video"  # Default webcam URL
BILLS_HISTORY_FILE = "bills_history.json"


def launch_main_window():
    window = tk.Tk()
    window.title("QuickBill System")
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
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
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
            billing_view.update_scanner_status("Scanner Stopped")

    def generate_bill():
        if not cart:
            messagebox.showwarning("Empty Cart", "No items to generate bill.")
            return
        try:
            generate_pdf_bill(cart)
            messagebox.showinfo("Bill Generated", "Bill has been generated and saved.")
            cart.clear()
            refresh_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill: {e}")

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

    billing_view = BillingView(
        content_container,
        {
            "generate_bill": generate_bill,
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

    import datetime

    bill_number = "QB-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

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
    product_tree.bind(
        "<Double-1>",
        lambda event: edit_selected_product()
    )

    # --- Find Bill View ---
    find_bill_frame = tk.Frame(content_container, bg="#e9ecef")

    # Back to Billing Button
    find_back_button_frame = tk.Frame(find_bill_frame, bg="#e9ecef")
    find_back_button_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Button(
        find_back_button_frame,
        text="← Back to Billing",
        font=("Helvetica", 10, "bold"),
        bg="#6c757d",
        fg="white",
        command=lambda: show_billing_view(),
    ).pack(side=tk.LEFT)

    # Find Bill Section
    find_bill_section = tk.LabelFrame(
        find_bill_frame,
        text="🔍 Find Bill",
        bg="white",
        fg="#2c3e50",
        font=("Helvetica", 12, "bold"),
        relief="flat",
    )
    find_bill_section.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    # Scanner and Manual Entry Controls
    scanner_control_frame = tk.Frame(find_bill_section, bg="white")
    scanner_control_frame.pack(fill=tk.X, padx=5, pady=5)

    bill_scanner_status = tk.StringVar(value="📷 Bill scanner not started")
    bill_scanner_label = tk.Label(
        scanner_control_frame,
        textvariable=bill_scanner_status,
        fg="#28a745",
        font=("Helvetica", 10, "bold"),
        bg="white",
    )
    bill_scanner_label.pack(pady=5)

    tk.Button(
        scanner_control_frame,
        text="▶ Start Bill Scan",
        bg="#007bff",
        command=lambda: start_bill_scan(),
        width=12,
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(
        scanner_control_frame,
        text="■ Stop Bill Scan",
        bg="#dc3545",
        command=lambda: stop_bill_scan(),
        width=12,
    ).pack(side=tk.LEFT, padx=5)

    # Manual Bill Number Entry
    manual_bill_frame = tk.Frame(find_bill_section, bg="white")
    manual_bill_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(
        manual_bill_frame,
        text="Bill Number:",
        font=("Helvetica", 10, "bold"),
        bg="white",
    ).pack(side=tk.LEFT, padx=5)
    bill_number_var = tk.StringVar()
    bill_number_entry = tk.Entry(
        manual_bill_frame,
        textvariable=bill_number_var,
        font=("Helvetica", 10),
        width=20,
    )
    bill_number_entry.pack(side=tk.LEFT, padx=5)

    def search_manual_bill():
        barcode = bill_number_var.get().strip()
        if barcode:
            on_bill_barcode_detected(barcode)

    tk.Button(
        manual_bill_frame,
        text="Search",
        bg="#28a745",
        fg="white",
        command=search_manual_bill,
        width=8,
    ).pack(side=tk.LEFT, padx=5)

    # Bill Details Table
    bill_details_frame = tk.Frame(find_bill_section, bg="white")
    bill_details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    bill_columns = ("Item", "Quantity", "Price", "Total")
    bill_details_tree = ttk.Treeview(
        bill_details_frame, columns=bill_columns, show="headings", height=12
    )
    bill_details_tree.column("Item", width=300, anchor="w")
    bill_details_tree.column("Quantity", width=100, anchor="center")
    bill_details_tree.column("Price", width=100, anchor="center")
    bill_details_tree.column("Total", width=100, anchor="center")
    for col in bill_columns:
        bill_details_tree.heading(col, text=col)
    bill_details_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    bill_vsb = ttk.Scrollbar(
        bill_details_frame, orient="vertical", command=bill_details_tree.yview
    )
    bill_details_tree.configure(yscrollcommand=bill_vsb.set)
    bill_vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def start_bill_scan():
        global scanner_active
        if not scanner_active:
            scanner_active = True
            status_bar.scanner_connected()
            status_bar.set_status("Scanning Bill")
            scan_barcode_background(webcam_url, on_bill_barcode_detected)

    def stop_bill_scan():
        global scanner_active
        if scanner_active:
            stop_scanner()
            scanner_active = False
            status_bar.scanner_disconnected()
            status_bar.set_status("Ready")

    def on_bill_barcode_detected(barcode):
        global scanner_active
        bill_number_var.set(barcode)
        bill_details_tree.delete(*bill_details_tree.get_children())
        bill_data = find_bill_details(barcode)
        if bill_data:
            items, subtotal, tax, discount, total = bill_data
            for item in items:
                bill_details_tree.insert(
                    "",
                    "end",
                    values=(
                        item["name"],
                        item["qty"],
                        f"₹ {item['price']:.2f}",
                        f"₹ {item['total']:.2f}",
                    ),
                )
            bill_details_tree.insert(
                "", "end", values=("", "", "", ""), tags=("spacer",)
            )
            bill_details_tree.insert(
                "",
                "end",
                values=("Subtotal", "", "", f"₹ {subtotal:.2f}"),
                tags=("bold",),
            )
            bill_details_tree.insert(
                "", "end", values=("Tax (18%)", "", "", f"₹ {tax:.2f}"), tags=("bold",)
            )
            bill_details_tree.insert(
                "",
                "end",
                values=("Discount (5%)", "", "", f"₹ {discount:.2f}"),
                tags=("bold",),
            )
            bill_details_tree.insert(
                "", "end", values=("Total", "", "", f"₹ {total:.2f}"), tags=("bold",)
            )
            bill_scanner_status.set(f"✅ Bill found: {barcode}")
        else:
            bill_details_tree.insert("", "end", values=("No bill found", "", "", ""))
            bill_scanner_status.set(f"❌ Bill not found: {barcode}")
        stop_scanner()
        scanner_active = False
        bill_scanner_status.set("🛑 Bill scanner stopped")

    bill_details_tree.tag_configure("bold", font=("Helvetica", 9, "bold"))
    bill_details_tree.tag_configure("spacer", background="#e9ecef")

    def find_bill_details(bill_no):
        try:
            if not os.path.exists(BILLS_HISTORY_FILE):
                return None
            with open(BILLS_HISTORY_FILE, "r", encoding="utf-8") as f:
                bills = json.load(f)
            for bill in bills:
                if bill["bill_no"] == bill_no:
                    items = bill["items"]
                    subtotal = bill["subtotal"]
                    tax = bill["tax"]
                    discount = bill["discount"]
                    total = bill["total"]
                    return items, subtotal, tax, discount, total
            return None
        except Exception as e:
            print(f"[ERROR] Failed to read bill history: {e}")
            return None

    toolbar = Toolbar(
        window,
        {
            "new_bill": (
                clear_cart_all if "clear_cart_all" in locals() else lambda: None
            ),
            "save_bill": lambda: None,
            "print_bill": lambda: None,
            "hold_bill": lambda: None,
            "find_bill": lambda: show_find_bill_view(),
            "products": lambda: show_settings_view(),
            "settings": lambda: show_settings_view(),
            "customers": lambda: None,
            "reports": lambda: None,
            "exit": window.destroy,
        },
    )

    toolbar.pack(fill="x")

    # --- View Switching Functions ---
    def show_billing_view():
        settings_frame.pack_forget()
        find_bill_frame.pack_forget()
        billing_view.pack(fill=tk.BOTH, expand=True)
        window.title("QuickBill System - Billing")
        if scanner_active:
            billing_view.update_scanner_status("Scanner Active")
        else:
            billing_view.update_scanner_status("Ready")

    def show_settings_view():

        global scanner_active

        refresh_product_table()  # <-- ADD THIS FIRST

        billing_view.pack_forget()

        find_bill_frame.pack_forget()

        settings_frame.pack(fill=tk.BOTH, expand=True)

        window.title("QuickBill System - Products")

        if scanner_active:

            stop_scanner()

            scanner_active = False

    def show_find_bill_view():
        global scanner_active
        billing_view.pack_forget()
        settings_frame.pack_forget()
        find_bill_frame.pack(fill=tk.BOTH, expand=True)
        window.title("QuickBill System - Find Bill")
        if scanner_active:
            stop_scanner()
            scanner_active = False
        bill_scanner_status.set("📷 Bill scanner not started")
        bill_number_var.set("")
        bill_details_tree.delete(*bill_details_tree.get_children())

    def show_about():
        messagebox.showinfo(
            "About",
            "QuickBill v1.0\nModern Python Billing App\nBy https://github.com/kartikbansode/",
        )

    def show_help():
        messagebox.showinfo(
            "Help",
            "- Use barcode scanner or manual entry to add items.\n- Use +/– to adjust quantity.\n- Click 🗑 to delete item.\n- Use Generate Bill to save.\n- Use Settings > Settings to configure.\n- Use Bills > Find Bill with scanner or manual entry to view past bills.",
        )

    # ---------------- Toolbar ----------------

    def dummy():
        pass

    # Initialize with billing view

    show_billing_view()
    window.mainloop()
