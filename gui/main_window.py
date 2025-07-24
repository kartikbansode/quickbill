import tkinter as tk
from tkinter import ttk, messagebox
from logic.cart import cart, add_to_cart, remove_from_cart, update_quantity
from logic.billing import calculate_totals
from logic.barcode_scanner import scan_barcode_background, stop_scanner, play_beep
from logic.database import get_product_by_barcode
from logic.pdf_generator import generate_pdf_bill
import threading
import datetime

scanner_active = False

def launch_main_window():
    window = tk.Tk()
    window.title("QuickBill - Billing System")
    window.geometry("1000x720")
    window.configure(bg="white")

    def update_clock():
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        time_label.config(text=current_time)
        window.after(1000, update_clock)

    # Title bar
    title_frame = tk.Frame(window, bg="white")
    title_frame.pack(fill=tk.X, pady=(10, 5))

    tk.Label(title_frame, text="🧾 QuickBill Billing Software", font=("Helvetica", 20, "bold"),
             bg="white", fg="#2c3e50").pack(side=tk.LEFT, padx=20)

    time_label = tk.Label(title_frame, font=("Helvetica", 10), bg="white", fg="gray")
    time_label.pack(side=tk.RIGHT, padx=20)
    update_clock()

    # Scrollable cart area
    cart_frame = tk.Frame(window, bg="white")
    cart_frame.pack(fill=tk.BOTH, expand=True, padx=10)

    canvas = tk.Canvas(cart_frame, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(cart_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Totals
    total_frame = tk.Frame(window, bg="#f6f6f6", bd=1, relief=tk.SOLID)
    total_frame.pack(fill=tk.X, pady=10, padx=10, ipady=5)

    subtotal_var = tk.StringVar()
    tax_var = tk.StringVar()
    discount_var = tk.StringVar()
    total_var = tk.StringVar()

    for label, var in zip(["Subtotal", "Tax", "Discount", "Total"],
                          [subtotal_var, tax_var, discount_var, total_var]):
        inner = tk.Frame(total_frame, bg="#f6f6f6")
        inner.pack(side=tk.LEFT, padx=20)
        tk.Label(inner, text=f"{label}:", font=("Helvetica", 10, "bold"), bg="#f6f6f6").pack()
        tk.Label(inner, textvariable=var, font=("Helvetica", 10), bg="#f6f6f6", fg="black").pack()

    # Scanner status
    scanner_status = tk.StringVar(value="📷 Scanner not started")
    scanner_label = tk.Label(window, textvariable=scanner_status, font=("Helvetica", 10), bg="white", fg="gray")
    scanner_label.pack(pady=(0, 5))

    def refresh_table():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for i, item in enumerate(cart):
            item_frame = tk.Frame(scrollable_frame, bg="white", pady=5, bd=1, relief=tk.SOLID)
            item_frame.pack(fill=tk.X, padx=5, pady=4)

            tk.Label(item_frame, text=item['name'], width=25, anchor="w", bg="white", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=5)
            tk.Label(item_frame, text=f"₹ {item['price']:.2f}", width=10, anchor="center", bg="white", font=("Helvetica", 10)).pack(side=tk.LEFT)
            tk.Label(item_frame, text=f"{item['qty']}", width=6, anchor="center", bg="white", font=("Helvetica", 10)).pack(side=tk.LEFT)

            tk.Label(item_frame, text=f"₹ {item['total']:.2f}", width=12, anchor="center", bg="white", font=("Helvetica", 10)).pack(side=tk.LEFT)

            btn_frame = tk.Frame(item_frame, bg="white")
            btn_frame.pack(side=tk.RIGHT, padx=10)

            tk.Button(btn_frame, text="+", width=3, command=lambda i=i: (update_quantity(i, cart[i]['qty'] + 1), refresh_table())).pack(side=tk.LEFT)
            tk.Button(btn_frame, text="-", width=3, command=lambda i=i: (update_quantity(i, cart[i]['qty'] - 1), refresh_table()) if cart[i]['qty'] > 1 else None).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="🗑", width=3, command=lambda i=i: (remove_from_cart(i), refresh_table())).pack(side=tk.LEFT)

        update_totals()

    def update_totals():
        subtotal, tax, disc, total = calculate_totals()
        subtotal_var.set(f"₹ {subtotal:.2f}")
        tax_var.set(f"₹ {tax:.2f}")
        discount_var.set(f"₹ {disc:.2f}")
        total_var.set(f"₹ {total:.2f}")

    def on_barcode_detected(barcode):
        product = get_product_by_barcode(barcode)
        if product:
            name, price = product[1], product[2]
            add_to_cart(name, price)
            play_beep()
            scanner_status.set(f"✅ Scanned: {barcode}")
            scanner_label.config(fg="green")
            refresh_table()
        else:
            scanner_status.set(f"❌ Not found: {barcode}")
            scanner_label.config(fg="red")

    def start_scan():
        global scanner_active
        scanner_active = True
        scanner_status.set("📡 Scanner active... Show barcode")
        scanner_label.config(fg="#007acc")
        scan_barcode_background("http://192.168.1.4:8080/video", on_barcode_detected)

    def stop_scan():
        global scanner_active
        stop_scanner()
        scanner_active = False
        scanner_status.set("🛑 Scanner stopped")
        scanner_label.config(fg="gray")

    def generate_bill():
        if not cart:
            messagebox.showwarning("Empty Cart", "No items to generate bill.")
            return
        generate_pdf_bill(cart)
        messagebox.showinfo("Bill Generated", "Bill has been generated and saved.")
        cart.clear()
        refresh_table()

    def clear_cart_all():
        if messagebox.askyesno("Clear Cart", "Are you sure you want to clear the cart?"):
            cart.clear()
            refresh_table()

    def show_about():
        messagebox.showinfo("About", "QuickBill v1.0\nDeveloped in Python for small retail businesses.")

    def show_help():
        messagebox.showinfo("Help", "➡ Start scanner\n➡ Hold barcode in front of camera\n➡ Adjust quantity using + / -\n➡ Remove using 🗑")

    # Buttons
    button_frame = tk.Frame(window, bg="white")
    button_frame.pack(pady=10)

    for label, command in [
        ("Start Scan", start_scan),
        ("Stop Scan", stop_scan),
        ("Generate Bill", generate_bill),
        ("Clear Cart", clear_cart_all),
        ("Help", show_help),
        ("About", show_about)
    ]:
        tk.Button(button_frame, text=label, width=15, font=("Helvetica", 10), command=command).pack(side=tk.LEFT, padx=10)

    refresh_table()
    window.mainloop()
