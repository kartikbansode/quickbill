import tkinter as tk
from tkinter import ttk, messagebox
from logic.cart import cart, add_to_cart, remove_from_cart
from logic.billing import calculate_totals
from logic.barcode_scanner import scan_barcode_background
from logic.database import get_product_by_barcode
from logic.pdf_generator import generate_pdf_bill
import threading

def launch_main_window():
    window = tk.Tk()
    window.title("QuickBill - Billing System")
    window.geometry("800x600")

    # Table
    tree = ttk.Treeview(window, columns=("Item", "Price", "Qty", "Total"), show="headings")
    for col in ("Item", "Price", "Qty", "Total"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Totals
    subtotal_var = tk.StringVar()
    tax_var = tk.StringVar()
    discount_var = tk.StringVar()
    total_var = tk.StringVar()

    tk.Label(window, text="Subtotal:").pack()
    tk.Label(window, textvariable=subtotal_var).pack()

    tk.Label(window, text="Tax:").pack()
    tk.Label(window, textvariable=tax_var).pack()

    tk.Label(window, text="Discount:").pack()
    tk.Label(window, textvariable=discount_var).pack()

    tk.Label(window, text="Total:").pack()
    tk.Label(window, textvariable=total_var).pack()

    # Scanner status
    scanner_status = tk.StringVar()
    scanner_status.set("📷 Scanner not started")
    tk.Label(window, textvariable=scanner_status, fg="green", font=("Arial", 10)).pack(pady=5)

    # Button actions
    def refresh_table():
        tree.delete(*tree.get_children())
        for item in cart:
            tree.insert('', tk.END, values=(item['name'], item['price'], item['qty'], item['total']))

        subtotal, tax, disc, total = calculate_totals()
        subtotal_var.set(f"₹ {subtotal:.2f}")
        tax_var.set(f"₹ {tax:.2f}")
        discount_var.set(f"₹ {disc:.2f}")
        total_var.set(f"₹ {total:.2f}")

    def delete_selected():
        selected = tree.selection()
        if selected:
            index = tree.index(selected[0])
            remove_from_cart(index)
            refresh_table()

    def scan_barcode_and_add():
        scanner_status.set("📡 Starting scanner...")

        def scan_thread():
            stream_url = "http://192.168.1.4:8080/video"  # ✅ Replace with your real phone stream
            barcode = scan_barcode_background(stream_url)

            if barcode:
                product = get_product_by_barcode(barcode)
                if product:
                    name, price = product[1], product[2]
                    add_to_cart(name, price)
                    refresh_table()
                    scanner_status.set(f"✅ Scanned: {barcode}")
                else:
                    scanner_status.set(f"❌ Not found: {barcode}")
            else:
                scanner_status.set("⚠️ Scan timeout or failed")

        threading.Thread(target=scan_thread, daemon=True).start()

    def generate_bill():
        if not cart:
            messagebox.showwarning("Empty Cart", "No items to generate bill.")
            return
        generate_pdf_bill(cart)
        messagebox.showinfo("Bill Generated", "Bill has been generated and saved.")
        cart.clear()
        refresh_table()

    # Buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Scan Barcode", command=scan_barcode_and_add).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Remove Selected", command=delete_selected).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Generate Bill", command=generate_bill).pack(side=tk.LEFT, padx=10)

    refresh_table()
    window.mainloop()
