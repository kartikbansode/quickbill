import tkinter as tk
from tkinter import ttk, messagebox
from logic.cart import cart, add_to_cart, remove_from_cart, update_quantity
from logic.billing import calculate_totals
from logic.barcode_scanner import scan_barcode_background, stop_scanner, play_beep
from logic.database import get_product_by_barcode
from logic.pdf_generator import generate_pdf_bill
import datetime

scanner_active = False

def launch_main_window():
    window = tk.Tk()
    window.title("QuickBill - Billing System")
    window.geometry("1100x750")
    window.configure(bg="#f4f6f9")

    # --- Clock Updater ---
    def update_clock():
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        time_label.config(text=now)
        window.after(1000, update_clock)

    # --- Title Section ---
    title_frame = tk.Frame(window, bg="#f4f6f9")
    title_frame.pack(pady=10, fill=tk.X)
    tk.Label(title_frame, text="🧾 QuickBill Billing Software", font=("Arial", 22, "bold"), fg="#2c3e50", bg="#f4f6f9").pack()
    time_label = tk.Label(title_frame, fg="gray", bg="#f4f6f9", font=("Arial", 10))
    time_label.pack()
    update_clock()

    # --- Item Section ---
    item_section = tk.LabelFrame(window, text="📦 Item List", bg="white", fg="#2c3e50", font=("Arial", 12, "bold"))
    item_section.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    columns = ("Item", "Price", "Qty", "Total")
    tree = ttk.Treeview(item_section, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

    vsb = ttk.Scrollbar(item_section, orient="vertical", command=tree.yview)
    tree.configure(yscroll=vsb.set)
    vsb.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)

    # --- Buttons beside Item List ---
    control_container = tk.Frame(item_section, bg="white")
    control_container.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

    def refresh_table():
        tree.delete(*tree.get_children())
        for i, item in enumerate(cart):
            tree.insert('', 'end', iid=str(i), values=(item['name'], f"₹ {item['price']:.2f}", item['qty'], f"₹ {item['total']:.2f}"))
        update_totals()
        draw_item_controls()

    def draw_item_controls():
        for widget in control_container.winfo_children():
            widget.destroy()
        for i, item in enumerate(cart):
            row = tk.Frame(control_container, bg="white")
            row.pack(fill=tk.X, pady=6)

            tk.Label(row, text=item['name'], width=18, anchor="w", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT)

            tk.Button(row, text="+", width=3, height=1, font=("Arial", 10), bg="#58d68d", fg="white",
                      command=lambda idx=i: update_item_qty(idx, +1)).pack(side=tk.LEFT, padx=2)

            tk.Label(row, text=f"{item['qty']}", width=3, font=("Arial", 10), bg="white").pack(side=tk.LEFT)

            tk.Button(row, text="-", width=3, height=1, font=("Arial", 10), bg="#f4d03f", fg="black",
                      command=lambda idx=i: update_item_qty(idx, -1)).pack(side=tk.LEFT, padx=2)

            tk.Button(row, text="🗑", width=3, height=1, font=("Arial", 10), bg="#ec7063", fg="white",
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

    # --- Totals Section ---
    totals_frame = tk.LabelFrame(window, text="💵 Totals", bg="white", fg="#2c3e50", font=("Arial", 12, "bold"))
    totals_frame.pack(fill=tk.X, padx=10, pady=10)

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
        subframe.pack(side=tk.LEFT, padx=30, pady=5)
        tk.Label(subframe, text=label, font=("Arial", 10, "bold"), bg="white").pack()
        tk.Label(subframe, textvariable=var, font=("Arial", 11), bg="white", fg="black").pack()

    # --- Scanner Status ---
    scanner_status = tk.StringVar(value="📷 Scanner not started")
    tk.Label(window, textvariable=scanner_status, fg="green", font=("Arial", 10), bg="#f4f6f9").pack(pady=5)

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

    # --- Controls Section ---
    control_frame = tk.LabelFrame(window, text="🎛️ Controls", bg="white", fg="#2c3e50", font=("Arial", 12, "bold"))
    control_frame.pack(padx=10, pady=10, fill=tk.X)

    tk.Button(control_frame, text="▶ Start Scan", bg="#aed6f1", command=lambda: start_scan(), width=14).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(control_frame, text="■ Stop Scan", bg="#f5b7b1", command=lambda: stop_scan(), width=14).pack(side=tk.LEFT, padx=10)
    tk.Button(control_frame, text="🧾 Generate Bill", bg="#d5f5e3", command=lambda: generate_bill(), width=16).pack(side=tk.LEFT, padx=10)
    tk.Button(control_frame, text="🧹 Clear Cart", bg="#f9e79f", command=lambda: clear_cart_all(), width=14).pack(side=tk.LEFT, padx=10)
    tk.Button(control_frame, text="❓ Help", command=lambda: show_help(), width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(control_frame, text="ℹ About", command=lambda: show_about(), width=10).pack(side=tk.LEFT, padx=10)

    def start_scan():
        global scanner_active
        scanner_status.set("📡 Scanner active... Show barcode")
        scanner_active = True
        scan_barcode_background("http://192.168.1.4:8080/video", on_barcode_detected)

    def stop_scan():
        global scanner_active
        stop_scanner()
        scanner_active = False
        scanner_status.set("🛑 Scanner stopped")

    def generate_bill():
        if not cart:
            messagebox.showwarning("Empty Cart", "No items to generate bill.")
            return
        generate_pdf_bill(cart)
        messagebox.showinfo("Bill Generated", "Bill has been generated and saved.")
        cart.clear()
        refresh_table()

    def clear_cart_all():
        if messagebox.askyesno("Clear All", "Are you sure you want to clear the entire cart?"):
            cart.clear()
            refresh_table()

    def show_about():
        messagebox.showinfo("About", "QuickBill v1.0\nModern Python Billing App\nBy @YourName")

    def show_help():
        messagebox.showinfo("Help", "- Use barcode scanner to scan items.\n- Use +/– to adjust quantity.\n- Click 🗑️ to delete item.\n- Click Generate Bill to save.")

    refresh_table()
    window.mainloop()
