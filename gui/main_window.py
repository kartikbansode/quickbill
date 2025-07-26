import tkinter as tk
from tkinter import ttk, messagebox
from logic.cart import cart, add_to_cart, remove_from_cart, update_quantity
from logic.billing import calculate_totals
from logic.barcode_scanner import scan_barcode_background, stop_scanner, play_beep
from logic.database import get_product_by_barcode, add_product, edit_product, delete_product, get_all_products
import datetime
from logic.pdf_generator import generate_pdf_bill
import os
import json

scanner_active = False
webcam_url = "http://192.168.1.7:8080/video"  # Default webcam URL
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
    style.configure("TButton", font=("Helvetica", 10, "bold"), padding=8, background="#007bff", foreground="white")
    style.map("TButton", background=[("active", "#0056b3")])
    style.configure("TLabelFrame", font=("Helvetica", 11, "bold"), foreground="#2c3e50", background="white")
    style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#007bff", foreground="white")
    style.configure("Bold.Treeview", font=("Helvetica", 9, "bold"))

    # --- Menu Bar ---
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)

    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=window.quit)

    # Settings Menu
    settings_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Settings", command=lambda: show_settings_view())

    # Bills Menu
    bills_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Bills", menu=bills_menu)
    bills_menu.add_command(label="Find Bill", command=lambda: show_find_bill_view())

    # Help Menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=lambda: show_help())
    help_menu.add_command(label="About", command=lambda: show_about())

    # --- Clock Updater ---
    def update_clock():
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        time_label.config(text=now)
        window.after(1000, update_clock)

    # --- Title Section ---
    title_frame = tk.Frame(window, bg="#007bff", relief="flat")
    title_frame.pack(fill=tk.X)
    tk.Label(title_frame, text="QuickBill System", font=("Helvetica", 20, "bold"), fg="white", bg="#007bff").pack(side=tk.LEFT, padx=10, pady=10)
    time_label = tk.Label(title_frame, fg="white", bg="#007bff", font=("Helvetica", 10))
    time_label.pack(side=tk.RIGHT, padx=10)
    update_clock()

    # --- Content Container ---
    content_container = tk.Frame(window, bg="#e9ecef")
    content_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # --- Billing View ---
    billing_frame = tk.Frame(content_container, bg="#e9ecef")

    # Item Section
    item_section = tk.LabelFrame(billing_frame, text="Item List", bg="white", fg="#2c3e50", font=("Helvetica", 12, "bold"), relief="flat")
    item_section.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # Container for 50/50 split
    item_split_container = tk.Frame(item_section, bg="white")
    item_split_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Item List Table (Left, 50%)
    tree_frame = tk.Frame(item_split_container, bg="white")
    tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    columns = ("Item", "Price", "Qty", "Total")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
    tree.column("Item", width=300, anchor="w")
    tree.column("Price", width=100, anchor="center")
    tree.column("Qty", width=80, anchor="center")
    tree.column("Total", width=100, anchor="center")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side=tk.LEFT, fill=tk.Y)

    # Item Edit Controls (Right, 50%)
    control_container = tk.Frame(item_split_container, bg="white")
    control_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def refresh_table():
        tree.delete(*tree.get_children())
        for i, item in enumerate(cart):
            tree.insert("", "end", iid=str(i), values=(item["name"], f"₹ {item['price']:.2f}", item["qty"], f"₹ {item['total']:.2f}"))
        update_totals()
        draw_item_controls()

    def draw_item_controls():
        for widget in control_container.winfo_children():
            widget.destroy()
        for i, item in enumerate(cart):
            row = tk.Frame(control_container, bg="white")
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=item['name'][:30], anchor="w", font=("Helvetica", 9, "bold"), bg="white").pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            button_frame = tk.Frame(row, bg="white")
            button_frame.pack(side=tk.RIGHT, padx=5)
            tk.Button(button_frame, text="+", width=2, font=("Helvetica", 8, "bold"), bg="#28a745", fg="white",
                      command=lambda idx=i: update_item_qty(idx, +1)).pack(side=tk.LEFT, padx=2)
            tk.Label(button_frame, text=f"{item['qty']}", width=4, font=("Helvetica", 8), bg="white").pack(side=tk.LEFT)
            tk.Button(button_frame, text="-", width=2, font=("Helvetica", 8, "bold"), bg="#ffc107", fg="black",
                      command=lambda idx=i: update_item_qty(idx, -1)).pack(side=tk.LEFT, padx=2)
            tk.Button(button_frame, text="🗑", width=2, font=("Helvetica", 8), bg="#dc3545", fg="white",
                      command=lambda idx=i: delete_item(idx)).pack(side=tk.LEFT, padx=2)

    def update_item_qty(index, delta):
        current = cart[index]['qty']
        new_qty = current + delta
        if new_qty < 1:
            remove_from_cart(index)
        else:
            update_quantity(index, new_qty)
        refresh_table()

    def delete_item(index):
        remove_from_cart(index)
        refresh_table()

    # Totals Section
    totals_frame = tk.Frame(billing_frame, bg="white", relief="flat")
    totals_frame.pack(padx=5, pady=5, fill=tk.X)

    subtotal_var = tk.StringVar()
    tax_var = tk.StringVar()
    discount_var = tk.StringVar()
    total_var = tk.StringVar()

    def update_totals():
        subtotal, tax, discount, total = calculate_totals()
        subtotal_var.set(f"₹ {subtotal:.2f}")
        tax_var.set(f"₹ {tax:.2f}")
        discount_var.set(f"₹ {discount:.2f}")
        total_var.set(f"₹ {total:.2f}")

    for label, var in zip(["Subtotal:", "Tax:", "Discount:", "Total:"],
                          [subtotal_var, tax_var, discount_var, total_var]):
        subframe = tk.Frame(totals_frame, bg="white")
        subframe.pack(side=tk.LEFT, padx=20, pady=5)
        tk.Label(subframe, text=label, font=("Helvetica", 10, "bold"), bg="white").pack()
        tk.Label(subframe, textvariable=var, font=("Helvetica", 11), bg="white", fg="#2c3e50").pack()

    # Scanner and Manual Entry Section
    scanner_frame = tk.Frame(billing_frame, bg="#e9ecef")
    scanner_frame.pack(fill=tk.X, padx=5, pady=5)

    scanner_status = tk.StringVar(value="Scanner not started")
    scanner_label = tk.Label(scanner_frame, textvariable=scanner_status, fg="#28a745", font=("Helvetica", 10, "bold"), bg="#e9ecef")
    scanner_label.pack(pady=5)

    manual_entry_frame = tk.Frame(scanner_frame, bg="#e9ecef")
    manual_entry_frame.pack(fill=tk.X, padx=5)
    tk.Label(manual_entry_frame, text="Barcode:", font=("Helvetica", 10), bg="#e9ecef").pack(side=tk.LEFT, padx=5)
    manual_barcode_entry = tk.Entry(manual_entry_frame, width=20, font=("Helvetica", 10))
    manual_barcode_entry.pack(side=tk.LEFT, padx=5)

    def add_manual_barcode():
        barcode = manual_barcode_entry.get().strip()
        if barcode:
            on_barcode_detected(barcode)
            manual_barcode_entry.delete(0, tk.END)

    tk.Button(manual_entry_frame, text="Add", bg="#28a745", fg="white", command=add_manual_barcode, width=8).pack(side=tk.LEFT, padx=5)

    # Controls Section
    control_frame = tk.Frame(billing_frame, bg="#e9ecef")
    control_frame.pack(fill=tk.X, padx=5, pady=5)

    tk.Button(control_frame, text="Start Scan", bg="#007bff", command=lambda: start_scan(), width=12).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(control_frame, text="Stop Scan", bg="#dc3545", command=lambda: stop_scan(), width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Generate Bill", bg="#28a745", command=lambda: generate_bill(), width=14).pack(side=tk.RIGHT, padx=5)
    tk.Button(control_frame, text="Clear Cart", bg="#ffc107", fg="black", command=lambda: clear_cart_all(), width=12).pack(side=tk.LEFT, padx=5)

    # --- Settings View ---
    settings_frame = tk.Frame(content_container, bg="#e9ecef")

    # Back to Billing Button
    back_button_frame = tk.Frame(settings_frame, bg="#e9ecef")
    back_button_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Button(back_button_frame, text="← Back to Billing", font=("Helvetica", 10, "bold"), bg="#6c757d", fg="white", 
              command=lambda: show_billing_view()).pack(side=tk.LEFT)

    # Webcam URL Section
    url_frame = tk.LabelFrame(settings_frame, text="Webcam URL", font=("Helvetica", 11, "bold"), bg="white", fg="#2c3e50")
    url_frame.pack(padx=10, pady=5, fill=tk.X)

    tk.Label(url_frame, text="URL:", font=("Helvetica", 10), bg="white").pack(side=tk.LEFT, padx=5)
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
                scanner_status.set("📡 Scanner restarting with new URL...")
                scan_barcode_background(webcam_url, on_barcode_detected)
            messagebox.showinfo("Success", "Webcam URL updated successfully.")
        else:
            messagebox.showwarning("Invalid URL", "Please enter a valid webcam URL.")

    tk.Button(url_frame, text="Save", font=("Helvetica", 10, "bold"), bg="#28a745", fg="white", command=save_url).pack(side=tk.LEFT, padx=5)

    # Manage Products Section
    product_frame = tk.LabelFrame(settings_frame, text="Manage Products", font=("Helvetica", 11, "bold"), bg="white", fg="#2c3e50")
    product_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    product_columns = ("Barcode", "Name", "Price")
    product_tree = ttk.Treeview(product_frame, columns=product_columns, show="headings", height=12)
    product_tree.column("Barcode", width=150, anchor="center")
    product_tree.column("Name", width=250, anchor="w")
    product_tree.column("Price", width=100, anchor="center")
    for col in product_columns:
        product_tree.heading(col, text=col)
    product_tree.pack(fill=tk.BOTH, padx=5, pady=5)

    vsb_product = ttk.Scrollbar(product_frame, orient="vertical", command=product_tree.yview)
    product_tree.configure(yscrollcommand=vsb_product.set)
    vsb_product.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5))

    def refresh_product_table():
        product_tree.delete(*product_tree.get_children())
        for product in get_all_products():
            product_tree.insert('', 'end', values=(product[0], product[1], f"₹ {product[2]:.2f}"))

    # Input Fields
    input_frame = tk.Frame(product_frame, bg="white")
    input_frame.pack(fill=tk.X, padx=5, pady=5)

    tk.Label(input_frame, text="Barcode:", font=("Helvetica", 10), bg="white").pack(side=tk.LEFT)
    barcode_entry = tk.Entry(input_frame, width=15, font=("Helvetica", 10))
    barcode_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Name:", font=("Helvetica", 10), bg="white").pack(side=tk.LEFT)
    name_entry = tk.Entry(input_frame, width=25, font=("Helvetica", 10))
    name_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Price:", font=("Helvetica", 10), bg="white").pack(side=tk.LEFT)
    price_entry = tk.Entry(input_frame, width=10, font=("Helvetica", 10))
    price_entry.pack(side=tk.LEFT, padx=5)

    # Buttons
    button_frame = tk.Frame(product_frame, bg="white")
    button_frame.pack(fill=tk.X, padx=5, pady=5)

    def add_product_action():
        barcode = barcode_entry.get().strip()
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        if not barcode or not name or not price:
            messagebox.showwarning("Invalid Input", "All fields are required.")
            return
        success, message = add_product(barcode, name, price)
        messagebox.showinfo("Result", message) if success else messagebox.showerror("Error", message)
        if success:
            refresh_product_table()
            barcode_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)

    def edit_product_action():
        selected = product_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a product to edit.")
            return
        barcode = barcode_entry.get().strip()
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        if not barcode or not name or not price:
            messagebox.showwarning("Invalid Input", "All fields are required.")
            return
        success, message = edit_product(barcode, name, price)
        messagebox.showinfo("Result", message) if success else messagebox.showerror("Error", message)
        if success:
            refresh_product_table()
            barcode_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)

    def delete_product_action():
        selected = product_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a product to delete.")
            return
        barcode = str(product_tree.item(selected[0])['values'][0])
        print(f"[DEBUG] Deleting barcode from UI: {barcode}")
        success, message = delete_product(barcode)
        messagebox.showinfo("Result", message) if success else messagebox.showerror("Error", message)
        if success:
            refresh_product_table()
            barcode_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)

    def select_product(event):
        selected = product_tree.selection()
        if selected:
            values = product_tree.item(selected[0])['values']
            barcode_entry.delete(0, tk.END)
            barcode_entry.insert(0, str(values[0]))
            name_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            price_entry.delete(0, tk.END)
            price_entry.insert(0, str(values[2]).replace("₹ ", ""))

    product_tree.bind('<<TreeviewSelect>>', select_product)

    tk.Button(button_frame, text="Add", font=("Helvetica", 10, "bold"), bg="#28a745", fg="white", command=add_product_action).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Edit", font=("Helvetica", 10, "bold"), bg="#007bff", fg="white", command=edit_product_action).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete", font=("Helvetica", 10, "bold"), bg="#dc3545", fg="white", command=delete_product_action).pack(side=tk.LEFT, padx=5)

    refresh_product_table()

    # --- Find Bill View ---
    find_bill_frame = tk.Frame(content_container, bg="#e9ecef")

    # Back to Billing Button
    find_back_button_frame = tk.Frame(find_bill_frame, bg="#e9ecef")
    find_back_button_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Button(find_back_button_frame, text="← Back to Billing", font=("Helvetica", 10, "bold"), bg="#6c757d", fg="white", 
              command=lambda: show_billing_view()).pack(side=tk.LEFT)

    # Find Bill Section
    find_bill_section = tk.LabelFrame(find_bill_frame, text="🔍 Find Bill", bg="white", fg="#2c3e50", font=("Helvetica", 12, "bold"), relief="flat")
    find_bill_section.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    # Scanner and Manual Entry Controls
    scanner_control_frame = tk.Frame(find_bill_section, bg="white")
    scanner_control_frame.pack(fill=tk.X, padx=5, pady=5)

    bill_scanner_status = tk.StringVar(value="📷 Bill scanner not started")
    bill_scanner_label = tk.Label(scanner_control_frame, textvariable=bill_scanner_status, fg="#28a745", font=("Helvetica", 10, "bold"), bg="white")
    bill_scanner_label.pack(pady=5)

    tk.Button(scanner_control_frame, text="▶ Start Bill Scan", bg="#007bff", command=lambda: start_bill_scan(), width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(scanner_control_frame, text="■ Stop Bill Scan", bg="#dc3545", command=lambda: stop_bill_scan(), width=12).pack(side=tk.LEFT, padx=5)

    # Manual Bill Number Entry
    manual_bill_frame = tk.Frame(find_bill_section, bg="white")
    manual_bill_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(manual_bill_frame, text="Bill Number:", font=("Helvetica", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=5)
    bill_number_var = tk.StringVar()
    bill_number_entry = tk.Entry(manual_bill_frame, textvariable=bill_number_var, font=("Helvetica", 10), width=20)
    bill_number_entry.pack(side=tk.LEFT, padx=5)

    def search_manual_bill():
        barcode = bill_number_var.get().strip()
        if barcode:
            on_bill_barcode_detected(barcode)

    tk.Button(manual_bill_frame, text="Search", bg="#28a745", fg="white", command=search_manual_bill, width=8).pack(side=tk.LEFT, padx=5)

    # Bill Details Table
    bill_details_frame = tk.Frame(find_bill_section, bg="white")
    bill_details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    bill_columns = ("Item", "Quantity", "Price", "Total")
    bill_details_tree = ttk.Treeview(bill_details_frame, columns=bill_columns, show="headings", height=12)
    bill_details_tree.column("Item", width=300, anchor="w")
    bill_details_tree.column("Quantity", width=100, anchor="center")
    bill_details_tree.column("Price", width=100, anchor="center")
    bill_details_tree.column("Total", width=100, anchor="center")
    for col in bill_columns:
        bill_details_tree.heading(col, text=col)
    bill_details_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    bill_vsb = ttk.Scrollbar(bill_details_frame, orient="vertical", command=bill_details_tree.yview)
    bill_details_tree.configure(yscrollcommand=bill_vsb.set)
    bill_vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def start_bill_scan():
        global scanner_active
        if not scanner_active:
            bill_scanner_status.set("Scanner active")
            scanner_active = True
            scan_barcode_background(webcam_url, on_bill_barcode_detected)

    def stop_bill_scan():
        global scanner_active
        if scanner_active:
            stop_scanner()
            scanner_active = False
            bill_scanner_status.set("🛑 Bill scanner stopped")

    def on_bill_barcode_detected(barcode):
        global scanner_active
        bill_number_var.set(barcode)
        bill_details_tree.delete(*bill_details_tree.get_children())
        bill_data = find_bill_details(barcode)
        if bill_data:
            items, subtotal, tax, discount, total = bill_data
            for item in items:
                bill_details_tree.insert('', 'end', values=(item['name'], item['qty'], f"₹ {item['price']:.2f}", f"₹ {item['total']:.2f}"))
            bill_details_tree.insert('', 'end', values=("", "", "", ""), tags=("spacer",))
            bill_details_tree.insert('', 'end', values=("Subtotal", "", "", f"₹ {subtotal:.2f}"), tags=("bold",))
            bill_details_tree.insert('', 'end', values=("Tax (18%)", "", "", f"₹ {tax:.2f}"), tags=("bold",))
            bill_details_tree.insert('', 'end', values=("Discount (5%)", "", "", f"₹ {discount:.2f}"), tags=("bold",))
            bill_details_tree.insert('', 'end', values=("Total", "", "", f"₹ {total:.2f}"), tags=("bold",))
            bill_scanner_status.set(f"✅ Bill found: {barcode}")
        else:
            bill_details_tree.insert('', 'end', values=("No bill found", "", "", ""))
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
            with open(BILLS_HISTORY_FILE, 'r', encoding='utf-8') as f:
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

    # --- View Switching Functions ---
    def show_billing_view():
        settings_frame.pack_forget()
        find_bill_frame.pack_forget()
        billing_frame.pack(fill=tk.BOTH, expand=True)
        window.title("QuickBill System - Billing")
        if scanner_active:
            scanner_status.set("📡 Scanner active... Scan barcode")
        else:
            scanner_status.set("📷 Scanner not started")

    def show_settings_view():
        global scanner_active
        billing_frame.pack_forget()
        find_bill_frame.pack_forget()
        settings_frame.pack(fill=tk.BOTH, expand=True)
        window.title("QuickBill System - Settings")
        if scanner_active:
            stop_scanner()
            scanner_status.set("🛑 Scanner stopped")
            scanner_active = False

    def show_find_bill_view():
        global scanner_active
        billing_frame.pack_forget()
        settings_frame.pack_forget()
        find_bill_frame.pack(fill=tk.BOTH, expand=True)
        window.title("QuickBill System - Find Bill")
        if scanner_active:
            stop_scanner()
            scanner_active = False
        bill_scanner_status.set("📷 Bill scanner not started")
        bill_number_var.set("")
        bill_details_tree.delete(*bill_details_tree.get_children())

    # --- Scanner Functions ---
    def on_barcode_detected(barcode):
        product = get_product_by_barcode(barcode)
        if product:
            name, price = product[1], product[2]
            add_to_cart(name, price)
            play_beep()
            refresh_table()
            scanner_status.set(f"✅ Scanned: {barcode}")
        else:
            scanner_status.set(f"❌ Not found: {barcode}")

    def start_scan():
        global scanner_active
        if not scanner_active:
            scanner_status.set("📡 Scanner active... Scan barcode")
            scanner_active = True
            scan_barcode_background(webcam_url, on_barcode_detected)

    def stop_scan():
        global scanner_active
        if scanner_active:
            stop_scanner()
            scanner_active = False
            scanner_status.set("🛑 Scanner stopped")

    # --- Other Functions ---
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

    def clear_cart_all():
        if messagebox.askyesno("Clear All", "Are you sure you want to clear the entire cart?"):
            cart.clear()
            refresh_table()

    def show_about():
        messagebox.showinfo("About", "QuickBill v1.0\nModern Python Billing App\nBy https://github.com/kartikbansode/")

    def show_help():
        messagebox.showinfo("Help", "- Use barcode scanner or manual entry to add items.\n- Use +/– to adjust quantity.\n- Click 🗑 to delete item.\n- Use Generate Bill to save.\n- Use Settings > Settings to configure.\n- Use Bills > Find Bill with scanner or manual entry to view past bills.")

    # Initialize with billing view
    show_billing_view()
    window.mainloop()