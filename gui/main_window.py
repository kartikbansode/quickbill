import tkinter as tk
from tkinter import ttk, messagebox
from logic.cart import cart, add_to_cart, remove_from_cart
from logic.billing import calculate_totals
from logic.barcode_scanner import scan_barcode_background, stop_scanner, play_beep
from logic.database import get_product_by_barcode
from logic.pdf_generator import generate_pdf_bill
import threading
import datetime


def launch_main_window():
    window = tk.Tk()
    window.title("QuickBill - Billing System")
    window.geometry("1000x700")
    window.configure(bg="#f4f4f4")

    # Title Bar
    tk.Label(window, text="QuickBill POS", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white", pady=10).pack(fill=tk.X)

    # Timestamp
    time_label = tk.Label(window, text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), bg="#f4f4f4", font=("Arial", 10))
    time_label.pack(pady=2)

    # Table Frame
    table_frame = tk.Frame(window)
    table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(table_frame, columns=("Item", "Price", "Qty", "Total"), show="headings", height=15)
    for col in ("Item", "Price", "Qty", "Total"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Totals Frame
    totals_frame = tk.Frame(window, bg="#f4f4f4")
    totals_frame.pack(pady=10)

    subtotal_var = tk.StringVar()
    tax_var = tk.StringVar()
    discount_var = tk.StringVar()
    total_var = tk.StringVar()

    def add_total_row(label, var):
        row = tk.Frame(totals_frame, bg="#f4f4f4")
        row.pack(anchor="w")
        tk.Label(row, text=label, font=("Arial", 12), bg="#f4f4f4").pack(side=tk.LEFT, padx=5)
        tk.Label(row, textvariable=var, font=("Arial", 12, "bold"), fg="#333", bg="#f4f4f4").pack(side=tk.LEFT)

    for label, var in zip(["Subtotal:", "Tax:", "Discount:", "Total:"],
                          [subtotal_var, tax_var, discount_var, total_var]):
        add_total_row(label, var)

    # Scanner status
    scanner_status = tk.StringVar(value="📷 Scanner not started")
    tk.Label(window, textvariable=scanner_status, fg="green", font=("Arial", 10), bg="#f4f4f4").pack(pady=5)

    # Action Buttons
    button_frame = tk.Frame(window, bg="#f4f4f4")
    button_frame.pack(pady=10)

    def refresh_table():
        tree.delete(*tree.get_children())
        for i, item in enumerate(cart):
            tree.insert('', tk.END, iid=i, values=(item['name'], item['price'], item['qty'], item['total']))
        subtotal, tax, disc, total = calculate_totals()
        subtotal_var.set(f"₹ {subtotal:.2f}")
        tax_var.set(f"₹ {tax:.2f}")
        discount_var.set(f"₹ {disc:.2f}")
        total_var.set(f"₹ {total:.2f}")

    def delete_selected():
        selected = tree.selection()
        if selected:
            index = int(selected[0])
            remove_from_cart(index)
            refresh_table()

    def increase_qty():
        selected = tree.selection()
        if selected:
            index = int(selected[0])
            cart[index]['qty'] += 1
            cart[index]['total'] = cart[index]['qty'] * cart[index]['price']
            refresh_table()

    def decrease_qty():
        selected = tree.selection()
        if selected:
            index = int(selected[0])
            if cart[index]['qty'] > 1:
                cart[index]['qty'] -= 1
                cart[index]['total'] = cart[index]['qty'] * cart[index]['price']
                refresh_table()

    def clear_cart():
        cart.clear()
        refresh_table()

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
        scanner_status.set("📡 Starting scanner...")
        scan_barcode_background("http://192.168.1.4:8080/video", on_barcode_detected)

    def stop_scan():
        stop_scanner()
        scanner_status.set("🛑 Scanner stopped")

    def generate_bill():
        if not cart:
            messagebox.showwarning("Empty Cart", "No items to generate bill.")
            return
        generate_pdf_bill(cart)
        messagebox.showinfo("Bill Generated", "Bill has been generated and saved.")
        clear_cart()

    # Buttons
    tk.Button(button_frame, text="Start Scan", width=15, bg="#2196F3", fg="white", command=start_scan).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Stop Scan", width=15, bg="#f44336", fg="white", command=stop_scan).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="+ Qty", width=10, command=increase_qty).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="- Qty", width=10, command=decrease_qty).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete Item", width=15, command=delete_selected).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Clear Cart", width=15, command=clear_cart).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Generate Bill", width=15, bg="#4CAF50", fg="white", command=generate_bill).pack(side=tk.LEFT, padx=5)

    # Footer
    tk.Label(window, text="© 2025 QuickBill - Powered by OpenAI", font=("Arial", 8), bg="#f4f4f4", fg="#888").pack(pady=5)

    refresh_table()
    window.mainloop()